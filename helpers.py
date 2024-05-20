from typing import Dict


def get_char_list() -> Dict[int, str]:
    return get_list("txts/chars.txt")


def get_memo_list() -> Dict[int, str]:
    return get_list("txts/memoria_url_id.txt")


def get_filenames() -> Dict[int, str]:
    return get_list("txts/gift_text.txt")


def get_list(li: str) -> Dict[int, str]:
    names = {}
    with open(li, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.strip():
                _id, name = line.strip().split(";")
                names[int(_id)] = name
    return names
