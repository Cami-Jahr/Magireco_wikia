import concurrent.futures
import os
import ssl
import urllib.request as ur
from json import (
    dumps,
    loads)
from subprocess import (
    DEVNULL,
    Popen,
    STDOUT)

ssl._create_default_https_context = ssl._create_unverified_context

local_path_jp = "D:/OneDrive - NTNU/Private projects/Reverse Engineer/com.aniplex.magireco/files/madomagi/resource/"
local_path_en = "D:/OneDrive - NTNU/Private projects/Reverse Engineer/com.aniplex.magireco/files/madomagi/resource_en/"
online_path_jp = "https://android.magi-reco.com/magica/resource/download/asset/master/resource/"
online_path_en = "https://android.magica-us.com/magica/resource/download/asset/master/resource/"
temp_path = "D:/MagirecoTemps/"


def download_files(item, old_files, online_path, local_path):
    try:
        file = item["path"]
        file_list = item["file_list"]
        try:
            if old_files[file] == item["md5"]:
                return item
            else:
                print("E", end="")
        except KeyError:  # item not in old_files json
            pass
        # print("STARTING_FILE: {:<75}".format(file))

        path = "/".join(file.split("/")[:-1]) + "/"
        if not os.path.exists(local_path + path):
            os.makedirs(local_path + path)
            # print("CREATED_DICT: " + local_path + path)

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
                    stdout=DEVNULL,
                    stderr=STDOUT)
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
        return item
    except Exception as e:
        return e


def run(file_name, path, savepoint, online_path, local_path):
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
    complete_json = full_json + ongoing_json
    old_files = {}
    for _item in complete_json:
        old_files[_item["path"]] = _item["md5"]

    _request = ur.Request(path)
    json = loads(ur.urlopen(_request).read().decode("utf-8"))
    done = []
    length = len(json)
    nr = 0
    print(f"Total size of {file_name} is {length}. Savepoint sat to {savepoint}. Already have {len(old_files)} files")
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for items in [json[x:x + savepoint] for x in range(0, len(json), savepoint)]:
            nr += savepoint
            future_to_item = {executor.submit(download_files, item, old_files, online_path, local_path): item for item in items}
            for future in concurrent.futures.as_completed(future_to_item):
                item = future_to_item[future]
                if item is Exception:
                    raise item
                else:
                    done.append(item)
            print("{:.2f}% done with {}".format(min(100.0, nr / length * 100), file_name))
            with open("download_tracking/" + file_name + ".json", "w") as f:
                f.write(dumps(done))

    with open("download_tracking/" + file_name + ".json", "w") as f:
        f.write(dumps(done))
    with open("download_tracking/" + file_name + "_full.json", "w") as f:
        f.write(dumps(done))
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
    run_jp("files_prologue_voice", "asset_prologue_voice", 40)
    run_jp("files_prologue_main", "asset_prologue_main", 100)
    run_jp("files_movie_high", "asset_movieall_high", 25)
    run_jp("files_char_list", "asset_char_list", 30)
    run_jp("files_main", "asset_main", 500)
    run_jp("files_voice", "asset_voice", 600)
    run_jp("files_fullvoice", "asset_fullvoice", 600)
    # run_en("files_movie_high_en", "asset_movie_high", 50)
