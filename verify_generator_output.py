import json
import re
from collections import defaultdict


def remove_words_to_ignore(string):
    """Add words you want to ignore here"""
    return string \
        .replace("turn", "Turn") \
        .replace("  ", " ").strip()


def check_differences(keys, file, path_template, wiki_items, description, effect_values, order_dependents):
    x = 0
    differences = 0
    for line in reversed(file.readlines()):
        x += 1
        _id, item = line.strip().split(";")
        item = item.replace(" ", "_").replace("?", "%3F").replace(":", "..").replace("/", "-")
        item = ((item + '&') if item[-1] == '.' else item)
        path = path_template.format(item).replace(" ", "_")

        matches = {}
        try:
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
                    matches[key] = (generated_text, wikia_text)
        except FileNotFoundError:
            pass
        effect_replacements = {}
        effect_replacements_update = {}

        for order_dependent in order_dependents:
            orphans = defaultdict(list)
            childless = defaultdict(list)
            replacement_nrs = {}
            for nr in range(20):
                key = order_dependent.replace("NR", str(nr))
                if key in matches:
                    generated_text, wikia_text = matches[key]
                    if generated_text != wikia_text:
                        base_generated_text = re.sub("(\[.*?])", "", re.sub("(\(.*?\))", "", generated_text)).replace("  ", " ").strip()
                        base_wikia_text = re.sub("(\[.*?])", "", re.sub("(\(.*?\))", "", wikia_text)).replace("  ", " ").strip()
                        childless[base_generated_text].append(nr)
                        orphans[base_wikia_text].append(nr)
                    replacement_nrs[nr] = nr
                    effect_replacements[key] = key

            replacements_update = {}
            disconnected_generated = []
            disconnected_wikia = []
            for gen_text, gen_key in childless.items():
                if gen_text in orphans:
                    wikia_key = orphans[gen_text]
                    for i in range(min(len(gen_key), len(wikia_key))):
                        replacements_update[gen_key[i]] = wikia_key[i]

            # Marry effects without a partner
            gen_keys = set(replacements_update.keys())
            wikia_keys = set(replacements_update.values())
            for gen_key in gen_keys:
                if gen_key not in wikia_keys:
                    disconnected_generated.append(gen_key)
            for wikia_key in wikia_keys:
                if wikia_key not in gen_keys:
                    disconnected_wikia.append(wikia_key)
            for i in range(len(disconnected_generated)):
                replacements_update[disconnected_wikia[i]] = disconnected_generated[i]

            for from_id, to_id in replacements_update.items():
                effect_replacements_update[order_dependent.replace("NR", str(from_id))] = order_dependent.replace("NR", str(to_id))

            if order_dependent in effect_values:
                for nr in range(20):
                    if nr in replacements_update:
                        for effect_mask in effect_values[order_dependent]:
                            new_mask = effect_mask.replace("NR", str(replacements_update[nr]))
                            old_mask = effect_mask.replace("NR", str(nr))
                            for mr in range(20):
                                new_key = new_mask.replace("MR", str(mr))
                                old_key = old_mask.replace("MR", str(mr))
                                effect_replacements_update[old_key] = new_key
                            effect_replacements_update[old_mask] = new_mask

        effect_replacements.update(effect_replacements_update)

        for key in matches:
            generated_text = matches[key][0]
            wikia_text = matches[effect_replacements[key] if key in effect_replacements else key][1]
            if ignore_spaces:
                compare_generated_text = generated_text.replace(" ", "")
                compare_wikia_text = wikia_text.replace(" ", "")
            else:
                compare_generated_text = generated_text
                compare_wikia_text = wikia_text
            if compare_wikia_text != compare_generated_text:
                differences += 1
                diff_text = ""
                length = min(len(wikia_text), len(generated_text))
                for i in range(length):
                    diff_text += " " if wikia_text[i] == generated_text[i] else generated_text[i]
                diff_text += wikia_text[length:] + generated_text[length:]
                print(f"Incorrect for {description} with id={_id} {key}, {item}: \n\twiki: {wikia_text}\n\tgen:  {generated_text}\n\tdiff: {diff_text}")
    print(f"\n\nFound {differences} differences\n")


def check_incorrect_memos():
    """
    A function which compares field of generated memorias with their counterpart on the wikia
    To assure this is up-to-date run template_downloader.py#load_memos first"""

    with open("memos.json", "r", encoding="utf-8") as f:
        memos = json.load(f)

    # For easy filtering just input the keys you want to check
    keys = {
        "effect2",
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
        check_differences(keys, f, path_template, memos, "memo", {}, [])


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
        *["EX effect NR".replace("NR", str(nr)) for nr in range(1, 5)],
        *["Connect effect NR".replace("NR", str(nr)) for nr in range(1, 10)],
        *["Magia effect NR".replace("NR", str(nr)) for nr in range(1, 10)],
        *["Magia2 effect NR".replace("NR", str(nr)) for nr in range(1, 10)],
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

        *["EX effect NR".replace("NR", str(nr)) for nr in range(1, 5)],
        *["EX NR min".replace("NR", str(nr)) for nr in range(1, 5)],
        *["EX NR max".replace("NR", str(nr)) for nr in range(1, 5)],

        "Connect icon",
        *["Connect effect NR".replace("NR", str(nr)) for nr in range(1, 10)],
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
        *["Magia effect NR".replace("NR", str(nr)) for nr in range(1, 10)],
        *["Magia scaling NR".replace("NR", str(nr)) for nr in range(1, 10)],
        *["Magia 1 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 2 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 3 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 4 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 5 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 6 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 7 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 8 / NR".replace("NR", str(nr)) for nr in range(1, 6)],
        *["Magia 9 / NR".replace("NR", str(nr)) for nr in range(1, 6)],

        *["Magia2 effect NR".replace("NR", str(nr)) for nr in range(1, 10)],
        *["Magia2 NR".replace("NR", str(nr)) for nr in range(1, 10)],
    }

    effect_values = {
        "Connect effect NR": ["Connect NR / MR"],
        "Magia effect NR": ["Magia NR / MR", "Magia scaling NR"],
        "Magia2 effect NR": ["Magia2 NR"],
    }
    order_dependents = [
        "Connect effect NR",
        "Magia effect NR",
        "Magia2 effect NR",
        "Passive NR effect",
    ]

    path_template = "wikia_pages/characters/{0}/Template-{0}.txt"

    with open("txts/chars.txt", "r", encoding="utf-8") as f:
        check_differences(keys, f, path_template, girls, "char", effect_values, order_dependents)


ignore_spaces = True
check_incorrect_memos()
check_incorrect_chars()
