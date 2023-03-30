import os
import ssl
import urllib.request as ur
from json import (
    dumps,
    loads)
from multiprocessing import Process
from subprocess import (
    PIPE,
    Popen)

ssl._create_default_https_context = ssl._create_unverified_context

local_path_jp = "D:/OneDrive - NTNU/Private projects/Reverse Engineer/com.aniplex.magireco/files/madomagi/resource/"
local_path_en = "D:/OneDrive - NTNU/Private projects/Reverse Engineer/com.aniplex.magireco/files/madomagi/resource_en/"
online_path_jp = "https://android.magi-reco.com/magica/resource/download/asset/master/resource/"
online_path_en = "https://android.magica-us.com/magica/resource/download/asset/master/resource/"
temp_path = "D:/MagirecoTemps/"


def download_files(json, old_files, file_name, savepoint, online_path, local_path):
    old_path = ""
    done = []
    length = len(json)
    nr = 0
    show = 0
    print(f"Total size of {file_name} is {length}. Savepoint sat to {savepoint}. Already have {len(old_files)} files")
    for item in json:
        nr += 1
        show += 1
        file = item["path"]
        file_list = item["file_list"]
        try:
            if old_files[file] == item["md5"]:
                done.append(item)
                if show == savepoint:
                    show = 0
                    print("{:.2f}% done with {}".format(nr / length * 100, file_name))
                    with open("download_tracking/" + file_name + ".json", "w") as f:
                        f.write(dumps(done))
                continue
            else:
                print("E", end="")
        except KeyError:  # item not in old_files json
            pass
        print("STARTING_FILE: {:<75}".format(file), end="", flush=True)

        path = "/".join(file.split("/")[:-1]) + "/"
        if old_path != path:  # New path
            old_path = path
            if not os.path.exists(local_path + old_path):
                os.makedirs(local_path + old_path)
                print("CREATED_DICT: " + local_path + old_path)

        if len(file_list) > 1:
            paths = []
            for _f in file_list:
                path = _f['url']
                paths.append(temp_path + path)
                dicts = path.split("/")[:-1]
                created_path = temp_path
                for i in range(len(dicts)):
                    if not os.path.exists(created_path + dicts[i]):
                        os.makedirs(created_path + dicts[i])
                    created_path += dicts[i] + "/"
                with open(temp_path + path, "wb") as f:
                    request = ur.Request(online_path + path)
                    f.write(ur.urlopen(request).read())
            _type = file[-3:]
            if _type == "png" or _type == "jpg":
                Popen(
                    ['ffmpeg', "-y", "-i", 'concat:{}'.format("|".join(paths)), "-c", "copy", local_path + file],
                    stdout=PIPE,
                    stdin=PIPE)
            else:
                _object = b""
                for path in paths:
                    with open(path, "rb") as f:
                        _object += f.read()
                with open(local_path + file, "wb") as f:
                    f.write(_object)
        else:
            with open(local_path + file, "wb") as f:
                request = ur.Request(online_path + file_list[0]['url'])
                f.write(ur.urlopen(request).read())
        print("CREATED_FILE: " + file, flush=True)

        done.append(item)
        if show == savepoint:
            show = 0
            print("{:.2f}% done with {}".format(nr / length * 100, file_name))
            with open("download_tracking/" + file_name + ".json", "w") as f:
                f.write(dumps(done + old_files))
    with open("download_tracking/" + file_name + ".json", "w") as f:
        f.write(dumps(done))
    with open("download_tracking/" + file_name + "_full.json", "w") as f:
        f.write(dumps(done))


def run(file_name, path, nr, online_path, local_path):
    try:
        with open("download_tracking/" + file_name + ".json", "r") as f:
            ongoing_json = loads(f.read())
    except:
        ongoing_json = []
    try:
        with open("download_tracking/" + file_name + "_full.json", "r") as f:
            full_json = loads(f.read())
    except:
        full_json = []

    old_files = {}
    for _item in full_json + ongoing_json:
        old_files[_item["path"]] = _item["md5"]

    _request = ur.Request(path)
    online_json = loads(ur.urlopen(_request).read().decode("utf-8"))
    download_files(online_json, old_files, file_name, nr, online_path, local_path)
    print("\nJSON_IS_DONE: " + file_name + "\n")


def run_jp(file_name, source, nr):
    run(
        file_name, "https://android.magi-reco.com/magica/resource/download/asset/master/" + source + ".json",
        nr,
        online_path_jp,
        local_path_jp)


def run_en(file_name, source, nr):
    run(
        file_name, "https://android.magica-us.com/magica/resource/download/asset/master/" + source + ".json",
        nr,
        online_path_en,
        local_path_en)


if __name__ == '__main__':
    Process(target=run_jp, args=("files_main", "asset_main", 25)).start()
    # Process(target=run_jp, args=("files_voice", "asset_voice", 40)).start()
    # Process(target=run_jp, args=("files_prologue_voice", "asset_prologue_voice", 40)).start()
    Process(target=run_jp, args=("files_prologue_main", "asset_prologue_main", 40)).start()
    Process(target=run_jp, args=("files_char_list", "asset_char_list", 40)).start()
    # Process(target=run_jp, args=("files_fullvoice", "asset_fullvoice", 40)).start()
    Process(target=run_jp, args=("files_movie_high", "asset_movieall_high", 5)).start()
    # Process(target=run_en, args=("files_movie_high_en", "asset_movie_high", 5)).start()
