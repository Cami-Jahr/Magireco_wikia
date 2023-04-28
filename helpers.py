import requests
import re


def get_char_list():
    di = get_online_list("User:Thefrozenfish/Sandbox/CharacterListing")
    return di


def get_memo_list():
    return get_online_list("User:Thefrozenfish/Sandbox/MemoriaListing")


def get_filenames():
    return get_list("txts/gift_text.txt")


def get_list(li):
    names = {}
    with open(li, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.strip():
                _id, name = line.strip().split(";")
                names[int(_id)] = name
    return names


def get_online_list(li):
    names = {}
    text = requests.get('https://magireco.fandom.com/wiki/' + li).text
    for line in re.search(r'.*?<div class="mw-parser-output"><p>(.*?)</p>.*?', text, re.DOTALL).group(1).split("¤"):
        if line.strip():
            _id, name = line.strip().replace("&amp;", "&").split(";")
            names[int(_id)] = name
    return names
