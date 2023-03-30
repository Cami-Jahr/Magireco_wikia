import os
from subprocess import (
    PIPE,
    Popen)
from time import sleep

from helpers import get_char_list

cha = get_char_list()


def merge_files(path, target, base_target):
    dirs = sorted(os.listdir(path), reverse=True)
    files = []
    for doc in dirs:
        if ".wav" == doc[-4:] or ".adx" == doc[-4:] or ".m2v" == doc[-4:]:
            files.append(doc)
        else:
            try:
                merge_files(path + "/" + doc, target + "/" + doc, target)
            except NotADirectoryError:
                pass
    if files:
        run_config = ['ffmpeg', "-y"]
        for file in files:
            run_config += ["-i", "{}/{}".format(path, file)]
        f_name = path.split("/")[-1]
        made = False
        for _id in cha:
            if "char" in path and str(_id) in f_name:
                f_name = cha[_id] + f_name.split(str(_id))[1].replace("out", "")
                run_config += [base_target + "/" + f_name + ".mp4"]
                made = True
        if not made:
            run_config += [base_target + "/" + f_name + ".mp4"]
        if not os.path.isfile(run_config[-1]):
            print("making:", f_name)
            Popen(run_config, stdout=PIPE, stdin=PIPE)
            sleep(2)


base_original_path = "D:/OneDrive - NTNU/Private projects/Reverse Engineer/com.aniplex.magireco/files/madomagi/resource/movie"
base_target_path = "D:/OneDrive - NTNU/Private projects/Reverse Engineer/Video"
merge_files(base_original_path, base_target_path, base_target_path)

base_original_path = "D:/OneDrive - NTNU/Private projects/Reverse Engineer/com.aniplex.magireco/files/madomagi/resource_en/movie"
base_target_path = "D:/OneDrive - NTNU/Private projects/Reverse Engineer/Video_en"
# merge_files(base_original_path, base_target_path, base_target_path)
