#!/usr/bin/env python3
"""MiniSlurm client. Single node job queue client.

Usage:
  minislurm_client (socket <socket>|config <config>) add [--path=<path> --name=<name> --stdout=<stdout> \
--stderr=<stderr> --timeout=<timeout>] -- <args>...
  minislurm_client (socket <socket>|config <config>) add <base_name> [--path=<path> --timeout=<timeout>] -- <args>...
  minislurm_client (socket <socket>|config <config>) rm (--all | --id=<id> | --name <name>)
  minislurm_client (socket <socket>|config <config>) pause (--all | --id=<id> | --name <name>)
  minislurm_client (socket <socket>|config <config>) continue (--all | --id=<id> | --name=<name>)
  minislurm_client (socket <socket>|config <config>) list (--all | --clear | --command | --ids | --names \
| --id=<id> | --name=<name>)
  minislurm_client (-h | --help)
  minislurm_client --version

Options:
  -h --help            Show this screen.
  --version            Show version.
  --path=<path>        Execution path [default: .].
  --id=<id>            ID of job.
  --name=<name>        Name of job.
  --stdout=<stdout>    File to connect to job STDOUT.
  --stderr=<stderr>    File to connect to job STDERR.
  --timeout=<timeout>  Timeout before job is forcefully terminated.
"""

from docopt import docopt
from pathlib import Path
import socket
import configparser

version = "21.11"


def main():
    arguments = docopt(__doc__, version=f"MiniSlurm v{version}")

    if arguments["config"]:
        with open(arguments["<config>"], "r"):
            config = configparser.ConfigParser(inline_comment_prefixes=["#", ";"])
            config.read(arguments["<config>"])
            arguments["<socket>"] = config["SERVER"]["SOCKET"]
    skt = Path(arguments["<socket>"]).resolve()

    if not skt.exists():
        raise FileNotFoundError(f"socket {skt} does not exist")

    msg = []
    if arguments["add"]:
        exec_path = Path(arguments["--path"]).resolve()
        if not exec_path.exists():
            raise FileNotFoundError(f"directory {exec_path} does not exist")
        msg.append(f"add path {exec_path}")
        if arguments[f"<base_name>"] is not None:
            bname = arguments[f"<base_name>"]
            msg.append(f"name {bname} stdout {bname}.out stderr {bname}.err")
        else:
            for key in ["name", "stdout", "stderr"]:
                if arguments[f"--{key}"] is not None:
                    msg.append(key)
                    msg.append(arguments[f"--{key}"])
        if arguments["--timeout"] is not None:
            msg.append("timeout")
            msg.append(arguments["--timeout"].replace(" ", ""))
        msg.append("--")
        for arg in arguments["<args>"]:
            msg.append(f"'{arg}'")
    elif arguments["rm"] or arguments["pause"] or arguments["continue"]:
        for key in ["rm", "pause", "continue"]:
            if arguments[key]:
                msg.append(key)
        if arguments["--all"]:
            msg.append("all")
        else:
            for key in ["name", "id"]:
                if arguments[f"--{key}"] is not None:
                    msg.append(key)
                    msg.append(arguments[f"--{key}"])
    elif arguments["list"]:
        msg.append("list")
        for key in ["all", "command", "clear"]:
            if arguments[f"--{key}"]:
                msg.append(key)
        for key in ["name", "id"]:
            if arguments[f"--{key}"] is not None:
                msg.append(key)
                msg.append(arguments[f"--{key}"])
        for key in ["names", "ids"]:
            if arguments[f"--{key}"]:
                msg.append(key)

    msg = " ".join(msg) + "\n"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(str(skt))
        client.settimeout(5)

        client.sendall(msg.encode())
        try:
            data = client.recv(4096)
            print(data.decode().strip())
        except socket.timeout:
            print("Server not responding")
        client.close()


if __name__ == "__main__":
    main()
