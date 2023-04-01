import json
import re

import requests


def fetch_info(keys, file):
    x = 0
    dic = {key: {} for key in keys}

    for line in reversed(file.readlines()):
        x += 1
        _id, item = line.strip().split(";")
        r = requests.get('https://magireco.fandom.com/wiki/Template:' + item.replace(" ", "_").replace("?", r"%3F") + '?action=edit')
        for key in keys:
            text = re.findall(rf"{key} *= *(.*)", r.text)
            if len(text) < 1:
                # print("Error: ", 'https://magireco.fandom.com/wiki/Template:' + item.replace(" ", "_").replace("?", r"%3F") + '?action=edit', "\n", text, key)
                pass
            else:
                dic[key][_id] = text[0].replace("&amp;", "&").strip()
        print(f"{x:>3}", item)
    return dic


def load_memos():
    keys = [
        "image",
        "effect_name",
        "effect_name_JP",
        "effect1",
        "effect2",
        "Cooldown",
        "Cooldown2",
    ]

    with open("txts/memoria_url_id.txt", "r", encoding="utf-8") as f:
        dic = fetch_info(keys, f)

    with open("memos.json", "w", encoding="utf-8") as f:
        json.dump(dic, f, ensure_ascii=False)


def load_girls():
    keys = [
        *["Passive NR icon".replace("NR", str(nr)) for nr in range(1, 20)],
        *["Passive NR name".replace("NR", str(nr)) for nr in range(1, 20)],
        *["Passive NR name JP".replace("NR", str(nr)) for nr in range(1, 20)],
        *["Passive NR effect".replace("NR", str(nr)) for nr in range(1, 20)],

        "Active 1 icon",
        "Active 1 name",
        "Active 1 name JP",
        "Active 1 effect",
        "Active 1 cooldown",

        *["EX effect NR".replace("NR", str(nr)) for nr in range(1, 5)],
        *["EX NR min".replace("NR", str(nr)) for nr in range(1, 5)],
        *["EX NR max".replace("NR", str(nr)) for nr in range(1, 5)],

        "Connect icon",
        *["Connect 1 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 2 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 3 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 4 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 5 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 6 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 7 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 8 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 9 / NR".replace("NR", str(nr)) for nr in range(1, 6)],

        "Magia icon",
        *["Magia effect NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia scaling NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 1 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 2 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 3 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 4 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 5 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 6 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 7 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 8 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 9 / NR".replace("NR", str(nr)) for nr in range(1, 6)],

        *["Magia2 effect NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia2 NR".replace("NR", str(nr)) for nr in range(1, 6)],
    ]

    with open("txts/chars.txt", "r", encoding="utf-8") as f:
        dic = fetch_info(keys, f)

    with open("girls.json", "w", encoding="utf-8") as f:
        json.dump(dic, f, ensure_ascii=False)


load_girls()
load_memos()
