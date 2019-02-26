import time
import os
import datetime

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class AutoTest(PatternMatchingEventHandler):
    patterns = ['*.py']

    def process(self, event):
        os.system('pytest')

        now = datetime.datetime.now().strftime('%Y/%m/%d %I:%M %p')
        print(now)

    def on_modified(self, event):
        self.process(event)


def main():
    path = '.'
    observer = Observer()
    observer.schedule(AutoTest(), path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    main()
