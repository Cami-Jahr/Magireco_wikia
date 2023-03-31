import json
import re

# For easy filtering just input the keys you want to ignore
keys_to_ignore = {"effect1", "effect2"}

def check_incorrect_memos():
    """
    A function which compares field of generated memorias with their counterpart on the wikia
    To assure this is up-to-date run template_downloader.py#load_memos first"""

    with open("memos.json", "r", encoding="utf-8") as f:
        memos = json.load(f)

    keys = {
        "image",
        "effect_name",
        "effect_name_JP",
        "effect1",
        "effect2",
        "Cooldown",
        "Cooldown2",
    } - keys_to_ignore

    x = 0
    print(f"{'':29} Memoria {'':48} on wikia {'':46} generated")
    with open("txts/memoria_url_id.txt", "r", encoding="utf-8") as f:
        for line in reversed(f.readlines()):
            x += 1
            _id, memo = line.strip().split(";")
            memo = memo.replace(" ", "_").replace("?", "%3F").replace(":", "..").replace("/", "-")
            memo = ((memo + '&') if memo[-1] == '.' else memo)
            if _id in ("9002", "9001"):
                continue
            path = f"wikia_pages/memorias/{memo}/Template-{memo}.txt".replace(" ", "_")

            with open(path, "r", encoding="utf-8") as f:
                file_text = f.read()
                for key in keys:
                    text = re.findall(rf"{key} *= *(.*)", file_text)
                    generated_text = text[0].strip()
                    wikia_text = memos[key][_id].strip()
                    if wikia_text != generated_text:
                        print(f"Incorrect for {key:15} for {memo:50}: {wikia_text:50} -vs- {generated_text:50}")


check_incorrect_memos()
