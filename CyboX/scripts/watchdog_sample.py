import datetime
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

WATCHDIR = os.path.abspath(os.path.dirname("C:\WORK\GitHub\JenaCybOX\owl"))


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if os.path.basename(event.src_path) == 'owlDemoData.xml':
            d = datetime.datetime.today()
            print d.strftime('%Y/%m/%d %H:%M:%S') + ' converted.'
            return


if __name__ in '__main__':
    while 1:
        event_handler = ChangeHandler()
        observer = Observer()
        observer.schedule(event_handler,WATCHDIR,recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()