import os
from subprocess import (
    PIPE,
    Popen)

temp_location = "D:/MagirecoTemps/hcaTemps"
temp_files = set(os.listdir(temp_location))


def convert_from_hca_to_ogg(path, target):
    dirs = os.listdir(path)
    target_files = set(os.listdir(target))
    for doc in dirs:
        if ".hca" == doc[-4:]:
            temp_file = "{}/{}.wav".format(temp_location, doc[:-8])
            if f"{doc[:-8]}.wav" not in temp_files:
                Popen(['/VGM/test.exe', "-o", temp_file, "{}/{}".format(path, doc)], stdout=PIPE).stdout.read()
            if f"{doc[:-8]}.ogg" not in target_files:
                Popen(['/VGM/opusenc.exe', temp_file, "{}/{}.ogg".format(target, doc[:-8])], stdout=PIPE)
        else:
            if not os.path.exists(target + "/" + doc):
                os.makedirs(target + "/" + doc)
            convert_from_hca_to_ogg(path + "/" + doc, target + "/" + doc)


base_original_path = "D:/OneDrive - NTNU/Private projects/Reverse Engineer/com.aniplex.magireco/files/madomagi/" \
                     "resource/sound_native"
base_target_path = "D:/OneDrive - NTNU/Private projects/Reverse Engineer/Sound"
convert_from_hca_to_ogg(base_original_path, base_target_path)
