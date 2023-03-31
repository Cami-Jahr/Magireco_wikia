import os
import shutil
from json import loads
from pathlib import Path

from effect_translator import (
    jp_to_en,
    roman_to_full,
    translate,
    translate_jap_to_eng,
    translate_roman_to_ascii)
from helpers import (
    get_char_list,
    get_memo_list)

memoria_header = """{{ {{PAGENAME}} |Stats}}

{{MemoriaLore
"""

memoria_body = """
}}
{{MemoriaTrivia|}}
<!--
* Each Memoria equipped grants a bonus (Item Name) amount each battle for the (Event Name) event.
** Normal: Gain (Normal Gain) Bonus (Item Name)
** Max Limit Break: Gain (MLB Gain) Bonus (Item Name)
-->
</div> <!-- MUST NOT BE REMOVED, start of div is in template called by {{ {{PAGENAME}} |Stats}} -->
"""

template_header = """{{Memoria/{{{1|Stats}}}|{{{2|}}}|{{{3|}}}|{{{4|}}}|{{{5|}}}|{{{6|}}}|{{{7|}}}|{{{8|}}}|{{{9|}}}"""
template_body = """
| name = {0}
| ImageSrc = 
| Event = 

| Naname = 
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


def format_text(desc=""):
    return f"{memoria_header}| jp = {desc}\n| en = \n| na = {memoria_body}"


def template_format(_id, Ename, stats=""):
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


def read(piece, chars):
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
        illustrator = "None Listed"
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
        description_eng, icon = translate(description_jp, arts)
        en_full_description = ""
        for en_skill in description_eng:
            if en_full_description:
                en_full_description += " & "
            en_full_description += en_skill
            if description_eng[en_skill][0]:
                en_full_description += f" [{description_eng[en_skill][0]}]"
            if description_eng[en_skill][1]:
                en_full_description += f" ({description_eng[en_skill][1]})"

        skill_name_jp = piece[f"pieceSkill{i}"]["name"].strip()

        if old_cooldown == cooldown and old_description == description_jp:
            only_max_level = True
        else:
            old_cooldown = cooldown
            old_description = description_jp

        skill_name_en = skill_name_jp
        skill_name_en = translate_jap_to_eng(skill_name_en)
        skill_name_en = translate_roman_to_ascii(skill_name_en)
        for c in skill_name_en:
            if ord(c) > 200:  # means that skill_name_en text contains special non-ascii characters
                # print("missing translation for", piece["pieceId"], "?", repr(skill_name_en))
                # for c in skill_name_en:
                # print(ord(c), end=" ")
                # print()
                break

        skills.append((en_full_description, cooldown))

    return [desc, [rank, piece_name_jp, illustrator, owner, hp, attack, defence, icon, skill_name_en, skill_name_jp, only_max_level, *skills[0], *skills[1]]]


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


if __name__ == '__main__':
    chars = get_char_list()
    memos = get_memo_list()

    make_basic = {
        1533: "いちばんちっちゃな家族の証",
        1535: "きみの眼を見れば",
        1538: "今日という一生の思い出",
    }

    coll = get_json()
    m_list = sorted(list(coll))

    main_parent = os.path.join("wikia_pages", "memorias")
    try:
        shutil.rmtree(main_parent)
    except FileNotFoundError:
        pass

    for _id in m_list:
        try:
            del make_basic[_id]
        except KeyError:
            pass
        try:
            Ename = memos[_id]
        except KeyError:
            Ename = str(_id)
        print(_id, Ename)
        Fname = Ename.replace(" ", "_").replace("?", "%3F").replace(":", "..").replace("/", "-")
        if Fname[-1] == ".":
            Fname += "&"
        parent = os.path.join(main_parent, Fname)
        Path(parent).mkdir(parents=True, exist_ok=True)
        for page, text in (
                (f"{Fname}", format_text(coll[_id][0].replace("＠", "<br />").replace("@", "<br />"))),
                (f"Template-{Fname}", template_format(_id, Ename, coll[_id][1]))
        ):
            with open(os.path.join(parent, page + ".txt"), "w", encoding="utf-8-sig") as f:
                f.write(text)

    for _id, jname in make_basic.items():
        Ename = memos[_id]
        print(_id, Ename)
        Fname = Ename.replace(" ", "_").replace("?", "%3F").replace(":", "..").replace("/", "-")
        if Fname[-1] == ".":
            Fname += "&"
        parent = os.path.join(main_parent, Fname)
        Path(parent).mkdir(parents=True, exist_ok=True)
        for page, text in (
                (f"{Fname}", format_text()),
                (f"Template-{Fname}", template_format(_id, Ename))
        ):
            with open(os.path.join(parent, page + ".txt"), "w", encoding="utf-8-sig") as f:
                f.write(text)
