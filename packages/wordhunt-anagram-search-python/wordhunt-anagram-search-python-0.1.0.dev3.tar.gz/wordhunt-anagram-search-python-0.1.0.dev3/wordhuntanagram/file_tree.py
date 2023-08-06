import sys
import os
import platform
import json


def resource_path(relative_path, platform=platform.system()):
    if platform.lower() == 'win' or platform.lower() == 'windows':
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # runs in a pyinstaller bundle
            here_dir = sys._MEIPASS
            return here_dir + '\\' + relative_path
            # pickle_file = os.path.join(here_dir, relative_path)
        else:
            here_dir = os.path.dirname(__file__)
            return here_dir + '\\' + relative_path
            # pickle_file = path.join(here_dir, relative path)
    elif platform.lower() == 'macosx' or platform.lower() == 'darwin':
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # runs in a pyinstaller bundle
            here_dir = sys._MEIPASS
            return here_dir + '/' + relative_path
            # pickle_file = os.path.join(here_dir, relative_path)
        else:
            here_dir = os.path.dirname(__file__)
            return here_dir + '/' + relative_path
    elif platform.lower() == 'android' or platform.lower() == 'java':
        # noinspection PyUnresolvedReferences
        from android.storage import app_storage_path
        settings_path = app_storage_path()
        return settings_path + '/' + relative_path
        # pickle_file = os.path.join(here_dir, relative_path)
    elif platform.lower() == 'ios':
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # runs in a pyinstaller bundle
            here_dir = sys._MEIPASS
            return here_dir + '/' + relative_path
            # pickle_file = os.path.join(here_dir, relative_path)
        else:
            here_dir = os.path.dirname(__file__)
            return here_dir + '/' + relative_path
    elif platform.lower() == 'linux' or platform.lower() == 'linux2':
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # runs in a pyinstaller bundle
            here_dir = sys._MEIPASS
            return here_dir + '/' + relative_path
            # pickle_file = os.path.join(here_dir, relative_path)
        else:
            here_dir = os.path.dirname(__file__)
    else:
        return relative_path


def convert_txt_to_json(path1, path2):
    diction = {}
    with open(path1, 'r') as word_handler:
        for word in word_handler.readlines():
            diction[word.rstrip('\n').strip('\n')] = 1

    with open(path2, 'w+') as word_json_handler:
        json.dump(diction, word_json_handler)
    return diction