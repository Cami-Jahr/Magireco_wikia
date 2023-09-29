import os
from json import loads
from pathlib import Path

from effect_translator import (
    remove_repeated_target,
    translate,
    translate_jap_to_eng,
    translate_roman_to_ascii)
from helpers import (
    get_char_list,
    get_memo_list)
from wikibot import wikibot

memoria_header = """{{ {{PAGENAME}} |Stats}}

{{MemoriaLore
"""

memoria_body = """
}}
{{MemoriaTrivia|}}
"""

event_memoria_body_mlb = """* Each Memoria equipped grants a bonus (Item Name) amount each battle for the [[Event Name]] event.
** Max Limit Break: Gain {0} Bonus (Item Name)
"""

event_memoria_body_full = """* Each Memoria equipped grants a bonus (Item Name) amount each battle for the [[Event Name]] event.
** Normal: Gain {0} Bonus (Item Name)
** Max Limit Break: Gain {1} Bonus (Item Name)
"""

memoria_footer = "</div> <!-- MUST NOT BE REMOVED, start of div is in template called by {{ {{PAGENAME}} |Stats}} -->"

template_header = """{{Memoria/{{{1|Stats}}}|{{{2|}}}|{{{3|}}}|{{{4|}}}|{{{5|}}}|{{{6|}}}|{{{7|}}}|{{{8|}}}|{{{9|}}}"""
template_body = """
| name = {0}
| ImageSrc = 
| Event = 

| Jname = {2}
| Rarity = {1}
| ID = {18}
| Illust = {3}
| Owner = {4}

| min_HP = {5}
| min_ATK = {7}
| min_DEF = {9}
| max_HP = {6}
| max_ATK = {8}
| max_DEF = {10}

| image = {11}
| effect_name = {12}
| effect_name_JP = {13}
| effect1 = {14}
| effect2 = {16}
| Cooldown = {15}
| Cooldown2 = {17}
"""
template_footer = """}}"""


def format_text(desc="", event_bonus: tuple = None):
    if not event_bonus:
        return f"{memoria_header}| jp = {desc}\n| en = {memoria_body}{memoria_footer}"
    if len(event_bonus) == 1:  # index 0 is MLB, index 1 (if it exists) is base
        return f"{memoria_header}| jp = {desc}\n| en = {memoria_body}{event_memoria_body_mlb.format(event_bonus[0])}{memoria_footer}"
    return f"{memoria_header}| jp = {desc}\n| en = {memoria_body}{event_memoria_body_full.format(event_bonus[1], event_bonus[0])}{memoria_footer}"


def template_format(_id: int, Ename: str, stats=""):
    if stats:
        rank, piece_name_jp, illustrator, owner, hp, attack, defence, icon, skill_name_en, skill_name_jp, only_max_level, en_full_description1, cooldown1, \
            en_full_description2, cooldown2 = stats
        skill_name_en = skill_name_en.split("[")[0]
        skill_name_jp = skill_name_jp.split("[")[0]
    else:
        rank = piece_name_jp = illustrator = owner = hp = attack = defence = icon = skill_name_en = skill_name_jp = en_full_description1 = cooldown1 = \
            en_full_description2 = cooldown2 = ""
        only_max_level = False

    if hp.__class__ == int:
        hp2 = int(round(hp * 2.5, 0))
        attack2 = int(round(attack * 2.5, 0))
        defence2 = int(round(defence * 2.5, 0))
        if hp == 0 and defence == 0 and attack == 0:
            hp = ""
            defence = ""
            attack = ""
    else:
        hp2 = attack2 = defence2 = ""
    if only_max_level:
        hp = attack = defence = en_full_description1 = cooldown1 = ""

    return template_header + \
        template_body.format(
            Ename, rank, piece_name_jp, illustrator, owner, hp, hp2, attack, attack2, defence, defence2, icon, skill_name_en, skill_name_jp, en_full_description1,
            cooldown1,
            en_full_description2, cooldown2, _id) + \
        template_footer


def read(piece: dict, chars: dict):
    try:
        attack = piece["attack"]
    except Exception as e:
        print(piece["pieceId"], piece["pieceName"])
        raise e
    defence = piece["defense"]
    hp = piece["hp"]
    illustrator = piece["illustrator"]
    piece_name_jp = piece["pieceName"]
    rank = piece["rank"][-1]
    if "―" == illustrator or not illustrator:
        illustrator = "-"
    owner = ""
    if "charaList" in piece:
        for character_obj in piece["charaList"]:
            if owner:
                owner += "; "
            owner += chars[character_obj["charaId"]]
    desc = piece["description"]

    skills = []
    old_cooldown = "TEMPLATE"
    old_description = "TEMPLATE"
    only_max_level = False

    for i in ("", "2"):
        # print(f"pieceSkill{i}")
        arts = []
        for jp_skill in range(1, 10):
            try:
                arts.append(piece[f"pieceSkill{i}"][f"art{jp_skill}"])
            except KeyError:
                break
        try:
            cooldown = piece[f"pieceSkill{i}"]["intervalTurn"]
        except KeyError:
            cooldown = ""

        description_jp = piece[f"pieceSkill{i}"]["shortDescription"]
        description_eng, icon = translate(description_jp, arts, True, False)
        remove_repeated_target(description_eng)
        en_full_description = ""
        for en_skill in description_eng:
            if en_full_description:
                en_full_description += " & "
            en_full_description += en_skill[:-1]
            if description_eng[en_skill][0]:
                en_full_description += f" [{description_eng[en_skill][0]}]"
            if description_eng[en_skill][1]:
                en_full_description += f" ({description_eng[en_skill][1]})"
            if en_skill[:-1] == "CC Gain Up":
                en_full_description += " (Does Not Work on Supports)"

        skill_name_jp = piece[f"pieceSkill{i}"]["name"].strip()

        if old_cooldown == cooldown and old_description == description_jp:
            only_max_level = True
        else:
            old_cooldown = cooldown
            old_description = description_jp

        skill_name_en = skill_name_jp
        if 65 <= ord(skill_name_en[0]) <= 90:  # First char is uppercase English letter
            skill_name_en = skill_name_en[0] + " " + translate_jap_to_eng(skill_name_en[1:])
        else:
            skill_name_en = translate_jap_to_eng(skill_name_en)
        skill_name_en = translate_roman_to_ascii(skill_name_en)

        # for c in skill_name_en: Everything between ord and break was commented out already, so I commented the rest
        #     if ord(c) > 200:  # means that skill_name_en text contains special non-ascii characters
        #         print("missing translation for", piece["pieceId"], "?", repr(skill_name_en))
        #         for c in skill_name_en:
        #             print(ord(c), end=" ")
        #         print()
        #         break

        skills.append((en_full_description, cooldown))

        if 'pieceKind' in piece and piece['pieceKind'] == 'EVENT' and "eventArt1" in piece["pieceSkill"]:
            if not only_max_level:
                event_bonus = ((int(piece['pieceSkill2']["eventArt1"]["effectValue"] / 1000)),
                               int(piece['pieceSkill']["eventArt1"]["effectValue"] / 1000))
            else:
                event_bonus = (int(piece['pieceSkill2']["eventArt1"]["effectValue"] / 1000),)
        else:
            event_bonus = None

    return [desc, [rank, piece_name_jp, illustrator, owner, hp, attack, defence, icon, skill_name_en, skill_name_jp, only_max_level, *skills[0], *skills[1]], event_bonus]


def get_json():
    coll = {}
    with open("jsons/memoria.json", "r", encoding="utf-8-sig") as f:
        json = loads(f.read())
    for piece in json:
        if "hp" not in json[piece]:
            print(piece, "not obtained, skipping")
            continue
        coll[json[piece]["pieceId"]] = read(json[piece], chars)
    return coll


upload_new_files = False
refresh_local_files = True

if __name__ == '__main__':
    chars = get_char_list()
    memos = get_memo_list()

    coll = get_json()
    m_list = sorted(list(coll))

    main_parent = os.path.join("wikia_pages", "memorias")

    for _id in m_list:
        try:
            Ename = memos[_id]
        except KeyError:
            Ename = str(_id)
        print(Ename)
        Fname = Ename.replace(" ", "_").replace("?", "%3F").replace(":", "..").replace("/", "-")
        if Fname[-1] == ".":
            Fname += "&"
        parent = os.path.join(main_parent, Fname)
        Path(parent).mkdir(parents=True, exist_ok=True)
        for page, text in (
                (f"{Fname}", format_text(coll[_id][0].replace("＠", "<br />").replace("@", "<br />"), coll[_id][2])),
                (f"Template:{Fname}", template_format(_id, Ename, coll[_id][1]))):

            if refresh_local_files:
                local_file = page.replace(":", "-")
                with open(os.path.join(parent, local_file + ".txt"), "w", encoding="utf-8-sig") as f:
                    f.write(text)

            if upload_new_files:
                online_text = wikibot.download_text(page)
                if len(online_text) < 5:  # Only upload new files, aka replace files without length
                    wikibot.upload(page, text)

