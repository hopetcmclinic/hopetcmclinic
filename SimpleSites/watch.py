import time
import os
import sys
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def __init__(self, filename_to_run):
        self.filename_to_run = filename_to_run

    def on_any_event(self, event):
        if event.is_directory:
            return
        print(f'File {event.src_path} has been {event.event_type}')
        if event.event_type in ['created', 'modified', 'moved']:
            self.run_python_file()

    def run_python_file(self):
        print(f"Running {self.filename_to_run}")
        try:
            subprocess.run(['python', self.filename_to_run], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            

if __name__ == "__main__":
    directory_to_watch = os.path.dirname(os.path.realpath(__file__))
    filename_to_run = os.path.join(directory_to_watch, "publish.py")

    event_handler = MyHandler(filename_to_run)
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
