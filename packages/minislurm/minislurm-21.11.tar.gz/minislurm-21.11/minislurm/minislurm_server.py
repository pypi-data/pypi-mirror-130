#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from enum import Enum, auto
from os import unlink, environ, chmod, path
from re import error as ReError
from re import search, compile
from shlex import split
from socketserver import UnixStreamServer, StreamRequestHandler, ThreadingMixIn
from sys import exit, argv
from threading import Lock
from time import sleep
import configparser
import logging
import signal
import subprocess


def parse_timedelta(string):
    """Parse string into timedelta.

    Allowed units are: second (s), minute (m), hour (h), day (d), week (w)
    Default unit is minute.
    """
    if search(r"^\s*(\d+[\.,]?\d*|[\.,]\d+)\s*$", string):
        return timedelta(minutes=float(string.replace(",", ".")))
    else:
        time = {"s": 0, "m": 0, "h": 0, "d": 0, "w": 0}
        for u in time.keys():
            match = search(r"(?i)(\d+[\.,]?\d*|[\.,]\d+)\s*" + u, string)
            if match is not None:
                time[u] = float(match.groups()[0].replace(",", "."))
        return timedelta(seconds=time["s"],
                         minutes=time["m"],
                         hours=time["h"],
                         days=time["d"],
                         weeks=time["w"])


def populate_options(options, string):
    """Get keyword arguments from string."""
    keys = options.keys()
    optlist = split(string)
    while len(optlist) > 0:
        arg = optlist.pop(0)
        if arg in keys:
            try:
                options[arg] = optlist.pop(0)
            except IndexError:
                pass


class JobStatus(Enum):
    """Status of job in jobqueue."""

    UNASSIGNED = auto()
    QUEUED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    TERMINATING = auto()
    TERMINATED = auto()
    KILLED = auto()
    PAUSED = auto()
    HELD = auto()


class Job():
    """Job container."""

    def __init__(self, args, pth, name=None, stdout=None, stderr=None, timeout=None):
        """Init class."""
        self.id = -1
        self.args = args
        self.path = pth
        self.name = name
        self.stdout = path.join(pth, stdout) if stdout is not None else "/dev/null"
        self.stderr = path.join(pth, stderr) if stderr is not None else "/dev/null"
        self.stdout_fd = None
        self.stderr_fd = None
        self.command = ""
        self.status = JobStatus.UNASSIGNED
        self.timeout = timeout
        self.timestamp = None
        self.deadline = None
        self.handle = None
        self.return_code = 0

    def __enter__(self):
        """Open job file descriptors."""
        self.stdout_fd = None if self.stdout is None else open(self.stdout, "w")
        self.stderr_fd = None if self.stderr is None else open(self.stderr, "w")

    def __exit__(self, type, value, traceback):
        """Close job file descriptors."""
        if self.stdout_fd is not None and not self.stdout_fd.closed:
            self.stdout_fd.close
        if self.stderr_fd is not None and not self.stderr_fd.closed:
            self.stderr_fd.close

    def __del__(self):
        """Close job file descriptors."""
        if self.stdout_fd is not None and not self.stdout_fd.closed:
            self.stdout_fd.close
        if self.stderr_fd is not None and not self.stderr_fd.closed:
            self.stderr_fd.close

    @staticmethod
    def _header():
        """Return string representation header."""
        s = "|{:5s}|{:15s}|{:11s}|{:29s}|{:29s}|".format("ID", "NAME", "STATUS", "TIMESTAMP", "DEADLINE")
        return "\n".join(["_" * len(s), s, "-" * len(s)])

    def __str__(self):
        """Return string representation."""
        return (f"|{self.id:5d}|{self.name[:15]:15s}|{self.status.name:11s}|" +
                (f"{str(None):29s}|" if self.timestamp is None else f"{self.timestamp:%d-%m-%y %H:%M:%S (%Z)}|") +
                (f"{str(None):29s}|" if self.deadline is None else f"{self.deadline:%d-%m-%y %H:%M:%S (%Z)}|"))


class JobQueue():
    """Job queue."""

    def __init__(self, command_template, capacity, max_parallel, timeout, kill_timeout, timezone="UTC", callback=None):
        """Init class."""
        self.command_template = command_template
        self.nextid = 1
        self.queue = [None] * capacity
        self.running = 0
        self.max_parallel = max_parallel
        self.timeout = timeout
        self.kill_timeout = kill_timeout
        self.timezone = timezone
        self.mutex = Lock()
        self.callback = callback
        self.callback_ps = []

    def _now(self):
        """Return current time."""
        return datetime.now(self.timezone)

    def _place_item(self, item):
        """Place item in queue."""
        try:
            index = self.queue.index(None)
            self.queue[index] = item
        except ValueError:
            index = next(i for i, j in sorted(enumerate(self.queue), key=lambda x: x[1].id)
                         if j.status == JobStatus.COMPLETED or j.status == JobStatus.TERMINATED
                         or j.status == JobStatus.KILLED or j.status == JobStatus.FAILED)
            self.queue[index] = item

    def enqueue(self, job):
        """Add job to queue."""
        self.mutex.acquire()
        try:
            try:
                command = self.command_template.format(*job.args)
            except IndexError as e:
                raise ValueError("wrong number of arguments") from e
            with job as _:
                logging.debug(f"creating files {job.stdout} and {job.stderr}")
            try:
                self._place_item(job)
            except StopIteration as e:
                raise RuntimeError("queue is full") from e
            job.command = command
            job.status = JobStatus.QUEUED
            job.id = self.nextid
            self.nextid += 1
            job.name = str(job.id) if job.name is None else job.name
            if job.timeout is None:
                job.timeout = self.timeout
            job.timestamp = self._now()
            logging.info(f"Enqueued job {job.name} ID {job.id}")
            return job.id
        finally:
            self.mutex.release()

    def _start(self, job):
        """Start job."""
        job.timestamp = self._now()
        job.__enter__()
        proc = subprocess.Popen(split(job.command), cwd=job.path, stdout=job.stdout_fd, stderr=job.stderr_fd)
        job.deadline = self._now() + job.timeout
        return proc

    def _callback(self, job):
        """Start callback."""
        if self.callback is not None:
            try:
                self.callback_ps.append(subprocess.Popen(split(self.callback.format(job.name, job.id, job.status.name)),
                                                         cwd=job.path))
            except Exception as e:
                logging.error(f"Callback failed with error {e}")

    def stop(self, jobs):
        """Stop jobs."""
        self.mutex.acquire()
        try:
            jobs = [j for j in jobs if j.status == JobStatus.RUNNING or j.status == JobStatus.QUEUED]
            jobs_running = [j for j in jobs if j.status == JobStatus.RUNNING]
            jobs_queued = [j for j in jobs if j.status == JobStatus.QUEUED]
            for job in jobs_running:
                job.handle.send_signal(signal.SIGSTOP)
                job.status = JobStatus.PAUSED
                job.timestamp = self._now()
                logging.info(f"Paused job {job.name} ID {job.id}")
            for job in jobs_queued:
                job.status = JobStatus.HELD
                job.timestamp = self._now()
                logging.info(f"Held job {job.name} ID {job.id}")
            return len(jobs)
        finally:
            self.mutex.release()

    def cont(self, jobs):
        """Continue jobs."""
        self.mutex.acquire()
        try:
            jobs = [j for j in jobs if j.status == JobStatus.PAUSED or j.status == JobStatus.HELD]
            jobs_paused = [j for j in jobs if j.status == JobStatus.PAUSED]
            jobs_held = [j for j in jobs if j.status == JobStatus.HELD]
            for job in jobs_paused:
                job.handle.send_signal(signal.SIGCONT)
                job.status = JobStatus.RUNNING
                job.timestamp = self._now()
                logging.info(f"Continued job {job.name} ID {job.id}")
            for job in jobs_held:
                job.status = JobStatus.QUEUED
                job.timestamp = self._now()
                logging.info(f"Unheld job {job.name} ID {job.id} and assigned new ID {self.nextid}")
                job.id = self.nextid
                self.nextid += 1
            return len(jobs)
        finally:
            self.mutex.release()

    def terminate(self, jobs):
        """Terminate jobs."""
        self.mutex.acquire()
        try:
            jobs = [j for j in jobs if (j.handle is not None and
                                        (j.status == JobStatus.RUNNING or j.status == JobStatus.PAUSED))
                    or j.status == JobStatus.QUEUED or j.status == JobStatus.HELD]
            jobs_dequeue = [j for j in jobs if j.status == JobStatus.QUEUED or j.status == JobStatus.HELD]
            jobs_terminate = [j for j in jobs if j.status == JobStatus.RUNNING or j.status == JobStatus.PAUSED]
            self._dequeue(jobs_dequeue)
            self._terminate(jobs_terminate)
            return len(jobs)
        finally:
            self.mutex.release()

    def _terminate(self, jobs):
        """Terminate jobs."""
        for job in jobs:
            job.handle.send_signal(signal.SIGTERM)
            job.status = JobStatus.TERMINATING
            job.deadline = self._now() + self.kill_timeout
            job.timestamp = self._now()
            logging.info(f"Terminated job {job.name} ID {job.id}")

    def clear(self):
        """Clear finished jobs from queue."""
        self.mutex.acquire()
        try:
            jobs = [j for j in self.queue if j is not None
                    and (j.status == JobStatus.FAILED or j.status == JobStatus.TERMINATED
                       or j.status == JobStatus.KILLED or j.status == JobStatus.COMPLETED)]
            for job in jobs:
                i = self.queue.index(job)
                self.queue[i] = None
            logging.info("Cleared job queue")
            return len(jobs)
        finally:
            self.mutex.release()

    def _dequeue(self, jobs):
        """Dequeue jobs."""
        for job in jobs:
            job.status = JobStatus.TERMINATED
            job.timestamp = self._now()
            logging.info(f"Dequeued job {job.name} ID {job.id}")

    def _kill(self, job):
        """Kill job."""
        job.handle.send_signal(signal.SIGKILL)
        job.status = JobStatus.KILLED
        job.timestamp = self._now()
        logging.info(f"Killed job {job.name} ID {job.id}")

    def update(self):
        """Update status of jobs and maybe start new jobs."""
        self.mutex.acquire()
        try:
            self.callback_ps = [j for j in self.callback_ps if j.poll is None]  # avoid creating zombies
            for job in [j for j in self.queue if j is not None and j.status == JobStatus.RUNNING]:
                rv = job.handle.poll()
                if rv is not None:
                    job.status = JobStatus.COMPLETED if rv == 0 else JobStatus.FAILED
                    job.return_code = rv
                    self.running -= 1
                    self._callback(job)
                    logging.info(f"Finished job {job.name} ID {job.id}")
                else:
                    if job.deadline <= self._now():
                        self._terminate([job])
                        logging.warning(f"Timed out job {job.name} ID {job.id}")
            for job in [j for j in self.queue if j is not None and j.status == JobStatus.TERMINATING]:
                rv = job.handle.poll()
                if rv is not None:
                    job.status = JobStatus.TERMINATED
                    job.return_code = rv
                    self.running -= 1
                    self._callback(job)
                else:
                    if job.deadline <= self._now():
                        self._kill(job)
                        job.return_code = rv
                        self.running -= 1
                        self._callback(job)
            while self.running < self.max_parallel:
                try:
                    job = next(j for j in sorted([j for j in self.queue if j is not None], key=lambda x: x.id)
                               if j.status == JobStatus.QUEUED)
                    try:
                        job.handle = self._start(job)
                        job.status = JobStatus.RUNNING
                        self.running += 1
                        logging.info(f"Started job {job.name} ID {job.id}")
                    except Exception as e:
                        job.status = JobStatus.FAILED
                        logging.error(f"Cannot start job {job.name} ID {job.id}: {e}")
                except StopIteration:
                    break
        finally:
            self.mutex.release()

    def select(self, selector, select_by="id"):
        self.mutex.acquire()
        try:
            jobs = [j for j in self.queue if j is not None]
            if select_by.lower() == "id":
                return [j for j in jobs if selector.match(str(j.id)) is not None]
            elif select_by.lower() == "name":
                return [j for j in jobs if selector.match(j.name) is not None]
            else:
                return []
        finally:
            self.mutex.release()

    def list(self, jobs):
        """Return string representation of the selected jobs."""
        self.mutex.acquire()
        try:
            return "\n".join([Job._header()] + [str(j) for j in sorted(jobs, key=lambda j: j.id)])
        finally:
            self.mutex.release()

    def __str__(self):
        """Return string representation."""
        return self.list(sorted([j for j in self.queue if j is not None], key=lambda x: x.id))


class CommandTree():
    """Command tree element.

    Command tree element operates on a command string,
    parsing its first word and dispatching arguments  to one of the handlers.
    Each handler function takes a string input.
    Return values propagate to the top caller.
    """

    def __init__(self, default, handlers={}):
        """Init class."""
        self.default = default
        self.handlers = handlers

    def add_handler(self, command, function):
        """Add handler to command."""
        self.handlers[command] = function

    def __call__(self, line):
        """Dispatch command to handler."""
        try:
            command, args = line.split(" ", 1)
        except ValueError:
            command = line
            args = ""
        handler = self.handlers.get(command.strip())
        if handler is None:
            return self.default(line)
        else:
            return handler(args)


class Handler(StreamRequestHandler):
    """Server request handler."""

    def __init__(self, request, client_address, server):
        "Init class"
        global job_queue
        self.handler_tree = CommandTree(
            lambda _: "Unknown command. Use help to get list of commands",
            {"help": lambda _: "Available commands: help, add, rm, pause, continue, list",
             "add": CommandTree(
                 self.add_job,
                 {"help": lambda _: """Syntax: add path <dir> [name <name>] [stdout <file>] \
[stderr <file>] [timeout <time>] -- <args>"""}),
             "rm": CommandTree(
                 lambda _: """Syntax: rm (all|id <id>|name <name>)""",
                 {"help": lambda _: """Syntax: rm (all|id <id>|name <name>)""",
                  "all": lambda _: f"terminated jobs: {self.select(r'.*', job_queue.terminate)}",
                  "id": lambda selector: f"terminated jobs: {self.select(selector, job_queue.terminate)}",
                  "name": lambda selector: f"terminated jobs: {self.select(selector, job_queue.terminate, 'name')}"}
             ),
             "pause": CommandTree(
                 lambda _: """Syntax: pause (all|id <id>|name <name>)""",
                 {"help": lambda _: """Syntax: pause (all|id <id>|name <name>)""",
                  "all": lambda _: f"paused jobs: {self.select(r'.*', job_queue.stop)}",
                  "id": lambda selector: f"paused jobs: {self.select(selector, job_queue.stop)}",
                  "name": lambda selector: f"paused jobs: {self.select(selector, job_queue.stop, 'name')}"}
             ),
             "continue": CommandTree(
                 lambda _: """Syntax: continue (all|id <id>|name <name>)""",
                 {"help": lambda _: """Syntax: continue (all|id <id>|name <name>)""",
                  "all": lambda _: f"continued jobs: {self.select(r'.*', job_queue.cont)}",
                  "id": lambda selector: f"continued jobs: {self.select(selector, job_queue.cont)}",
                  "name": lambda selector: f"continued jobs: {self.select(selector, job_queue.cont, 'name')}"}
             ),
             "list": CommandTree(
                 lambda _: """Syntax: list (all|ids|names|clear|command|id <id>|name <name>)""",
                 {"help": lambda _: """Syntax: list (all|ids|names|clear|command|id <id>|name <name>""",
                  "all": lambda _: self.select(r".*", job_queue.list),
                  "id": lambda selector: self.select(selector, job_queue.list),
                  "ids": lambda _: self.select(r".*", lambda jobs: " ".join([str(j.id) for j in jobs])),
                  "name": lambda selector: self.select(selector, job_queue.list, "name"),
                  "names": lambda _: self.select(r".*", lambda jobs: " ".join({j.name for j in jobs})),
                  "command": lambda _: job_queue.command_template,
                  "clear": lambda _: f"cleared queue items: {job_queue.clear()}"}
             )}
        )
        super().__init__(request, client_address, server)

    def add_job(self, line):
        global job_queue
        try:
            opts, args = line.split("--", 1)
        except ValueError:
            return "Error: missing required fields"
        kvoptions = {"path": None, "name": None, "stdout": None, "stderr": None, "timeout": None}
        populate_options(kvoptions, opts)
        if kvoptions["path"] is None:
            return "Error: path is missing"
        kvoptions["timeout"] = None if kvoptions["timeout"] is None else parse_timedelta(kvoptions["timeout"])
        arglist = split(args)
        job = Job(arglist, kvoptions["path"], name=kvoptions["name"], timeout=kvoptions["timeout"],
                  stdout=kvoptions["stdout"],
                  stderr=kvoptions["stderr"])
        try:
            job_queue.enqueue(job)
            return f"Added job {job.name} with ID {job.id}"
        except Exception as e:
            return f"Error: {e}"

    def select(self, regex, action, select_by="id"):
        global job_queue
        try:
            selector = compile(regex)
            return action(job_queue.select(selector, select_by=select_by))
        except ReError as e:
            return f"Regex error: {e}"

    def handle(self):
        """Request handle."""
        try:
            while True:
                line = self.rfile.readline().strip()
                if len(line) == 0:
                    return
                self.request.sendall((self.handler_tree(line.decode()) + "\n").encode())
        except (ConnectionResetError, BrokenPipeError):
            return


class ThreadedUnixStreamServer(ThreadingMixIn, UnixStreamServer):
    """Server class."""

    def service_actions(self):
        """Timeout callback."""
        global job_queue
        job_queue.update()


def main():
    if len(argv) != 2:
        print("Configuration file is not provided")
        exit(1)

    global job_queue
    job_queue = None

    config = configparser.ConfigParser(inline_comment_prefixes=["#", ";"])
    config.read(argv[1])

    for section in ["SERVER", "PROGRAM"]:
        for cfg in config[section].keys():
            val = environ.get("_".join(["MINISLURM", section.upper(), cfg.upper()]))
            config[section][cfg] = config[section][cfg] if val is None else val

    log_level = getattr(logging, config["SERVER"]["LOG_LEVEL"].upper(), None)
    if not isinstance(log_level, int):
        raise ValueError(f"Invalid log level: {config['SERVER']['LOG_LEVEL']}")
    logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=log_level)

    def cleanup_function(_a, _b):
        """Cleanup on server stop."""
        global job_queue
        try:
            unlink(config["SERVER"]["SOCKET"])
        except FileNotFoundError:
            pass
        if job_queue is not None:
            job_queue.terminate(job_queue.select(compile(r'.*')))
            while job_queue.running > 0:
                job_queue.update()
                sleep(1)
        exit()

    signal.signal(signal.SIGINT, cleanup_function)
    signal.signal(signal.SIGHUP, cleanup_function)
    signal.signal(signal.SIGTERM, cleanup_function)

    job_queue = JobQueue(config["PROGRAM"]["COMMAND"],
                         int(config["SERVER"]["QUEUE_SIZE"]),
                         int(config["SERVER"]["MAX_PARALLEL"]),
                         parse_timedelta(config["PROGRAM"]["TIMEOUT"]),
                         parse_timedelta(config["PROGRAM"]["KILL_TIMEOUT"]),
                         timezone=timezone(timedelta(hours=int(config["SERVER"]["TIMEZONE_OFFSET"]))),
                         callback=config["SERVER"]["CALLBACK"] if len(config["SERVER"]["CALLBACK"]) > 0 else None)

    with ThreadedUnixStreamServer(config["SERVER"]["SOCKET"], Handler) as server:
        logging.info(f"Starting server with socket: {config['SERVER']['SOCKET']}")
        chmod(server.server_address, 0o770)
        server.serve_forever(int(config["SERVER"]["UPDATE_TIME"]))


if __name__ == "__main__":
    main()
