from Watchman import Watchman

if __name__ == '__main__':

    watch = Watchman()
    watch.set_setting_file("watchman.json")
    watch.watch()