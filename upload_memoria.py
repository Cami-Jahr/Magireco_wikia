from json import loads
from credentials import username, password
from upload_char import Uploader
from effect_translator import translate, jp_to_en, roman_to_full
from helpers import get_char_list, get_memo_list
from pathlib import Path
import os

text1 = """{{ {{PAGENAME}} |Stats}}

{{MemoriaLore
"""

text2 = """
}}

<!-- *This memoria features [[]]. --> <!-- Link and comma separate featured characters -->
<!--
* Each Memoria equipped grants a bonus (Item Name) amount each battle for the (Event Name) event.
** Normal: Gain (Normal Gain) Bonus (Item Name)
** Max Limit Break: Gain (MLB Gain) Bonus (Item Name)
-->
</div> <!-- MUST NOT BE REMOVED, start of div is in template called by {{ {{PAGENAME}} |Stats}} -->
"""

temp1 = """{{Memoria/{{{1|Stats}}}|{{{2|}}}|{{{3|}}}|{{{4|}}}|{{{5|}}}|{{{6|}}}|{{{7|}}}|{{{8|}}}|{{{9|}}}"""
temp2 = """
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
temp3 = """}}"""


def format_text(desc=""):
    return f"{text1}| jp = {desc}\n| en = \n| na = {text2}"


def template_format(_id, Ename, stats):
    rank, Jname, illu, owner, HP, ATK, DEF, icon, en, jp, st1, cd1, st2, cd2 = stats
    en = en.split("[")[0]
    jp = jp.split("[")[0]

    if HP.__class__ == int:
        HP2 = int(round(HP * 2.5, 0))
        ATK2 = int(round(ATK * 2.5, 0))
        DEF2 = int(round(DEF * 2.5, 0))
        if HP == 0 and DEF == 0 and ATK == 0:
            HP = ""
            DEF = ""
            ATK = ""
    else:
        HP2 = ""
        ATK2 = ""
        DEF2 = ""

    return temp1 + temp2.format(Ename, rank, Jname, illu, owner, HP, HP2, ATK, ATK2, DEF, DEF2, icon, en, jp, st1, cd1, st2, cd2, _id) + temp3


def read(piece, chars):
    try:
        atk = piece["attack"]
    except Exception as e:
        print(piece["pieceId"], piece["pieceName"])
        raise e
    de = piece["defense"]
    hp = piece["hp"]
    illu = piece["illustrator"]
    Jname = piece["pieceName"]
    rank = piece["rank"][-1]
    if "―" == illu or not illu:
        illu = "None Listed"
    owner = ""
    if "charaList" in piece:
        for obj in piece["charaList"]:
            if owner:
                owner += "; "
            owner += chars[obj["charaId"]]
    desc = piece["description"]
    
    skills = []
    for i in ("", "2"):
        #print(f"pieceSkill{i}")
        arts = []
        for j in range(1, 10):
            try:
                arts.append(piece[f"pieceSkill{i}"][f"art{j}"])
            except KeyError:
                break
        try:
            cd = piece[f"pieceSkill{i}"]["intervalTurn"]
        except KeyError:
            cd = ""
        eng, icon = translate(piece[f"pieceSkill{i}"]["shortDescription"], arts)
        st = ""
        for e in eng:
            if st:
                st += " & "
            st += e
            if eng[e][0]:
                st += f" [{eng[e][0]}]"
            if eng[e][1]:
                st += f" ({eng[e][1]})"

        jp = piece[f"pieceSkill{i}"]["name"].strip()
        #for s, f in roman_to_full.items():
        #    jp = jp.replace(s, f)
        en = jp
        for j, e in jp_to_en.items():
            en = en.replace(j, e)
        for s, f in roman_to_full.items():
            en = en.replace(s, f)
        for c in en:
            if ord(c) > 200:
                #print("missing translation for", piece["pieceId"], "?", repr(en))
                #for c in en:
                    #print(ord(c), end=" ")
                #print()
                break

        skills.append((st, cd))
    return [desc, [rank, Jname, illu, owner, hp, atk, de, icon, en, jp, *skills[0], *skills[1]]]

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

    up_memos = []
    if up_memos:
        S = Uploader()
        S.login(username, password)
    coll = get_json()
    m_list = sorted(list(coll))

    for _id in m_list:
        Ename = memos[_id]
        print(_id, Ename)
        Fname = Ename.replace(" ", "_").replace("?", "%3F").replace(":", "..").replace("/", "-")
        if Fname[-1] == ".":
            Fname += "&"
        parent = os.path.join("wikia_pages", "memorias", Fname)
        Path(parent).mkdir(parents=True, exist_ok=True)
        for page, text in (
                (f"{Fname}", format_text(coll[_id][0].replace("＠", "<br />").replace("@", "<br />"))),
                (f"Template-{Fname}", template_format(_id, Ename, coll[_id][1]))
                ):   
            with open(os.path.join(parent, page + ".txt"), "w", encoding="utf-8-sig") as f:
                f.write(text)

    for _id, Ename in up_memos:
        Ename = Ename.replace("?", "%3F")
        print(Ename)
        S.upload(Ename, format_text(coll[_id][0].replace("＠", "<br />").replace("@", "<br />")))
        S.upload("Template:" + Ename, template_format(_id, Ename, *coll[_id][1]))

    if up_memos:
        S.end()
