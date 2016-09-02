import os
import threading
import time
import json
import webbrowser
import sys

def error(*args, **kwargs):
    print("[Watchman Error] ",end='')
    print(*args, file=sys.stderr, **kwargs)

class FileMeta:
    def __init__(self, file_name):
        self.file_name = file_name
        self.last_modified_time = os.path.getmtime(file_name)

    def is_changed(self):
        print("checking {}".format(self.file_name))
        curr_modified_time = os.path.getmtime(self.file_name)
        if curr_modified_time != self.last_modified_time:
            self.last_modified_time = curr_modified_time
            return True
        else:
            return False


class Watchman:

    def __init__(self):
        self.watched_files = []
        self.index_html = None
        self.has_setting = False
        self.browser = None

    def __add_watch_file(self, file_name):
        self.watched_files.append(FileMeta(file_name))

    def __add_watch_folder(self, folder_name):
        for file in os.listdir(folder_name):
            full_path = os.path.join(folder_name, file)

            if os.path.isdir(full_path):
                self.__add_watch_folder(full_path)
            else:
                self.__add_watch_file(full_path)

    def add_watch_target(self, path):
        if os.path.isdir(path):
            self.__add_watch_folder(path)
        else:
            self.__add_watch_file(path)

    def set_setting_file(self, setting_file_path):
        with open(setting_file_path) as setting_file:
            setting = json.load(setting_file)

            for path in setting["watch_targets"]:
                self.add_watch_target(path)

            self.index_html = setting["index_html"]

            self.browser = setting["browser"]

        self.has_setting = True


    def handle(self):
        controller = webbrowser.get(self.browser)
        controller.open("file://"+self.index_html)

    def __check(self):
        while True:
            for i in self.watched_files:
                if i.is_changed():
                    print("file changed")
                    self.handle()
            time.sleep(1)

    def watch(self):
        if self.has_setting:
            t = threading.Thread(target=self.__check)
            t.daemon = False
            t.start()
        else:
            error("No watchman.json")



