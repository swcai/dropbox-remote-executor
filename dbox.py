#!/usr/bin/env python

import os
import time
import daemon
from os.path import join

SOURCE_PATH = "/opt/home/swcai/Dropbox/Public/source"
RESULT_FILE = "/opt/home/swcai/Dropbox/Public/results.txt"

def do_real_job(path, latency = 20):
    while True:
        # check if any new file in the specific folder
        results = []
        now = time.time()
        for root, dirs, files in os.walk(path):
            for name in filter(lambda n: (now - os.stat(join(root, n)).st_mtime <= latency), files):
                results.append(join(root, name))
        
        # execute the file if the file is valid
        if len(results) != 0:
            res = open(RESULT_FILE, 'a')
            for f in results:
                for line in open(f).readlines():
                    res.write('command: ' + line)
                    res.write(os.popen(line).read())
                    res.write('\n')
                    res.flush()
            res.close()

        # sleep for a while
        time.sleep(latency)

if __name__ == "__main__":
    with daemon.DaemonContext():
        do_real_job("/opt/home/swcai/Dropbox/Public/monitor", 5)
