#!/usr/bin/env python
'''
Created on 2015/02/17

@author: Makoto
'''

from __future__ import print_function

import time
import subprocess

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class MyHundler(PatternMatchingEventHandler):
    def __init__(self, command, patterns):
        super(MyHundler, self).__init__(patterns=patterns)
        self.command = command
    
    def _run_command(self):
        subprocess.call([self.command, ])
    
    def on_moved(self, event):
        self._run_command()
    
    def on_created(self, event):
        self._run_command()
    
    def on_deleted(self, event):
        self._run_command()
        
    def on_modified(self, event):
        self._run_command()

def watch(path, command, extension):
    event_handler = MyHundler(command, ["*"+extension])
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print "EXVEPTION"
        observer.stop()
    observer.join()

def check():
    code = 'cheking now'
    print code

if __name__ == '__main__':
    path = r"C:\WORK\GitHub\JenaCybOX\owl\owlDemoData.xml"
    watch(path, check(), ".txt")
        