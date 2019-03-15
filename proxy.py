#! /usr/bin/env python3

import subprocess
import signal
import json
import os


def proxy(user, host, address):
    try:
        print("{} {}@{}".format(address, user, host))
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
        for item in content:
            user = item.get("user", "")
            host = item.get("host", "")
            for address in item.get("proxys", []):
                targets.append({
                    "user": user,
                    "host": host,
                    "proxy": address
                })
    # kill previous process
    for target in targets:
        kill_process(target.get("proxy"))
    # print(targets)
    # proxy
    subs = []
    for target in targets:
        _sub = proxy(target.get("user"), target.get("host"), target.get("proxy"))
        if _sub:
            subs.append(_sub)

    def exit_kill(sig, frame):
        for sub, address in subs:
            sub.kill()
            print("{} exit {}".format(address, sub.wait()))
    for sig in [signal.SIGINT, signal.SIGHUP, signal.SIGTERM]:
        signal.signal(sig, exit_kill)
    signal.pause()


if __name__ == "__main__":
    main()
