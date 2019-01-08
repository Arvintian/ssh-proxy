#! /usr/bin/env python3

import subprocess
import signal
import json
import os


def proxy(user, host, address):
    try:
        print("proxy:{}".format(address))
        cmd = ["ssh", "-NL"]
        cmd.append(address)
        cmd.append("{}@{}".format(user, host))
        sub = subprocess.Popen(cmd)
        return sub, address
    except Exception as e:
        print("proxy:{} error".format(address))


def kill_process(grep_str):
    try:
        pid = subprocess.run(["pgrep", "-f", grep_str], capture_output=True).stdout.decode().strip()
        if pid:
            subprocess.run(["kill", "-9", pid])
            print("kill:{} {}".format(grep_str, pid))
    except Exception as e:
        print("kill:{} error".format(grep_str))


def main():
    targets = []
    user = ""
    host = ""
    config = "{}/{}".format(os.environ['HOME'], "proxy.json")
    with open(config, "r") as proxy_file:
        content = json.loads(proxy_file.read())
        user = content.get("user", "")
        host = content.get("host", "")
        targets = content.get("proxys", [])
    # kill previous process
    for target in targets:
        kill_process(target)
    # print(user, host, targets)
    # proxy
    subs = []
    for target in targets:
        _sub = proxy(user, host, target)
        if _sub:
            subs.append(_sub)

    def exit_kill(sig, frame):
        for sub, address in subs:
            sub.kill()
            print("proxy:{} exit {}".format(address, sub.wait()))
    for sig in [signal.SIGINT, signal.SIGHUP, signal.SIGTERM]:
        signal.signal(sig, exit_kill)
    signal.pause()


if __name__ == "__main__":
    main()
