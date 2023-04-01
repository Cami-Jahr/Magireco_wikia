import json
import re


def remove_words_to_ignore(string):
    """Add words you want to ignore here"""
    return string \
        .replace("turn", "Turn") \
        .replace("  ", " ").strip()


def check_differences(keys, file, path_template, wiki_items, description):
    x = 0
    differences = 0
    for line in reversed(file.readlines()):
        x += 1
        _id, item = line.strip().split(";")
        item = item.replace(" ", "_").replace("?", "%3F").replace(":", "..").replace("/", "-")
        item = ((item + '&') if item[-1] == '.' else item)
        if _id in ("9002", "9001"):
            continue
        path = path_template.format(item).replace(" ", "_")

        with open(path, "r", encoding="utf-8") as f:
            file_text = f.read()
            for key in keys:
                text = re.findall(rf"{key.replace('_', ' ')} *= *(.*)", file_text.replace("_", " "))
                if len(text) < 1:
                    continue
                generated_text = remove_words_to_ignore(text[0].strip())
                if _id not in wiki_items[key]:
                    continue
                wikia_text = remove_words_to_ignore(wiki_items[key][_id].strip())

                if wikia_text != generated_text:
                    differences += 1
                    diff_text = ""
                    length = min(len(wikia_text), len(generated_text))
                    for i in range(length):
                        diff_text += " " if wikia_text[i] == generated_text[i] else generated_text[i]
                    diff_text += wikia_text[length:] + generated_text[length:]
                    print(f"Incorrect for {description} with id={_id} {key}, {item}: \n\twiki: {wikia_text}\n\tgen:  {generated_text}\n\tdiff: {diff_text}")
    print(f"\n\nFound {differences} differences")


def check_incorrect_memos():
    """
    A function which compares field of generated memorias with their counterpart on the wikia
    To assure this is up-to-date run template_downloader.py#load_memos first"""

    with open("memos.json", "r", encoding="utf-8") as f:
        memos = json.load(f)

    # For easy filtering just input the keys you want to check
    keys = {
        "effect1",
        "effect2",
        "Cooldown",
        "Cooldown2",
    }

    # use if you want to check all keys
    all_keys = {
        "image",
        "effect_name",
        "effect_name_JP",
        "effect1",
        "effect2",
        "Cooldown",
        "Cooldown2",
    }

    path_template = "wikia_pages/memorias/{0}/Template-{0}.txt"

    with open("txts/memoria_url_id.txt", "r", encoding="utf-8") as f:
        check_differences(all_keys, f, path_template, memos, "memo")


def check_incorrect_chars():
    """
    A function which compares field of generated memorias with their counterpart on the wikia
    To assure this is up-to-date run template_downloader.py#load_girls first"""

    with open("girls.json", "r", encoding="utf-8") as f:
        girls = json.load(f)

    # For easy filtering just input the keys you want to check
    keys = {
        *["Passive NR effect".replace("NR", str(nr)) for nr in range(1, 20)],

        "Active 1 effect",
        "Active 1 cooldown",

        *["EX effect NR".replace("NR", str(nr)) for nr in range(1, 5)],
        *["EX NR min".replace("NR", str(nr)) for nr in range(1, 5)],
        *["EX NR max".replace("NR", str(nr)) for nr in range(1, 5)],

        *["Connect 1 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 2 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 3 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 4 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 5 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 6 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 7 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 8 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Connect 9 / NR".replace("NR", str(nr)) for nr in range(1, 6)],

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
    }

    # use if you want to check all keys
    all_keys = {
        *["Passive NR icon".replace("NR", str(nr)) for nr in range(1, 20)],
        *["Passive NR name".replace("NR", str(nr)) for nr in range(1, 20)],
        *["Passive NR name JP".replace("NR", str(nr)) for nr in range(1, 20)],
        *["Passive NR effect".replace("NR", str(nr)) for nr in range(1, 20)],

        "Active 1 icon",
        "Active 1 name",
        "Active 1 name JP",
        "Active 1 effect",
        "Active 1 cooldown",

        "EX name",
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
    }

    path_template = "wikia_pages/characters/{0}/Template-{0}.txt"

    with open("txts/chars.txt", "r", encoding="utf-8") as f:
        check_differences(all_keys, f, path_template, girls, "char")


check_incorrect_memos()
check_incorrect_chars()
