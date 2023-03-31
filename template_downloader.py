import json
import re

import requests


def load_memos():
    x = 0
    keys = [
        "image",
        "effect_name",
        "effect_name_JP",
        "effect1",
        "effect2",
        "Cooldown",
        "Cooldown2",
    ]
    dic = {key: {} for key in keys}

    with open("txts/memoria_url_id.txt", "r", encoding="utf-8") as f:
        for line in reversed(f.readlines()):
            x += 1
            _id, memo = line.strip().split(";")
            r = requests.get('https://magireco.fandom.com/wiki/Template:' + memo.replace(" ", "_").replace("?", r"%3F") + '?action=edit')
            for key in keys:
                text = re.findall(rf"{key} *= *(.*)", r.text)
                if len(text) < 1:
                    if key in ("effect1", "Cooldown", "Cooldown2"):
                        dic[key][_id] = ""
                        continue
                    print(
                        "Error: ", 'https://magireco.fandom.com/wiki/Template:' + memo.replace(" ", "_").replace("?", r"%3F") + '?action=edit', "\n", text, key)
                    return
                else:
                    dic[key][_id] = text[0].replace("&amp;", "&").strip()
            print(f"{x:>3}", memo)

    with open("memos.json", "w", encoding="utf-8") as f:
        json.dump(dic, f, ensure_ascii=False)


load_memos()
