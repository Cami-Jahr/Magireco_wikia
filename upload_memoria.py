from json import loads
from credentials import username, password
from upload_char import Uploader

text1 = """{{ {{PAGENAME}} |Stats}}

{{MemoriaLore
"""

text2 = """
}}

{{MemoriaTrivia}} <!-- Currently just header, leave. -->
<!-- *This memoria features [[]]. --> <!-- Link and comma separate featured characters -->
<!--
* Each Memoria equipped grants a bonus (Item Name) amount each battle for the (Event Name) event.
** Normal: Gain (Normal Gain) Bonus (Item Name)
** Max Limit Break: Gain (MLB Gain) Bonus (Item Name)
-->
</div>
"""

temp1 = """{{Memoria/{{{1|Stats}}}|{{{2|}}}"""
temp2 = """
|name = {}
|ImageSrc = 
|Event = 

|naname = 
|Jname = {}
|Rarity = {}
|ID = {}
|Illust = {}
|Owner = {}

|min_HP = {}
|min_ATK = {}
|min_DEF = {}
|max_HP = {}
|max_ATK = {}
|max_DEF = {}

|image = 
|effect_name = 
|effect1 = 
|effect2 = 
|Cooldown = {}
|Cooldown2 = {}
"""
temp3 = """}}"""


def format_text(desc=""):
    return text1 + (("|jp = " + desc) if desc else "") + text2


def template_format(_id, Ename, rank, Jname, illu="", owner="", HP="", ATK="", DEF="", CD1="", CD2=""):
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

    return temp1 + temp2.format(Ename, Jname, rank, _id, illu, owner, HP, ATK, DEF, HP2, ATK2, DEF2, CD1, CD2) + temp3


def read(piece, chars):
    atk = piece["attack"]
    de = piece["defense"]
    hp = piece["hp"]
    illu = piece["illustrator"]
    Jname = piece["pieceName"]
    rank = piece["rank"][-1]
    if "―" == illu or not illu:
        illu = "None Listed"
    try:
        owner = chars[piece["charaIds"]]
    except KeyError:
        owner = ""
    desc = piece["description"]
    try:
        cd1 = piece["pieceSkill"]["intervalTurn"]
        cd2 = piece["pieceSkill2"]["intervalTurn"]
    except KeyError:
        cd1 = ""
        cd2 = ""
    return [desc, [rank, Jname, illu, owner, hp, atk, de, cd1, cd2]]


def get_chars():
    coll = {}
    with open("chars.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            l = line.strip().split(";")
            coll[l[0]] = l[1]
    return coll


def get_json():
    with open("../../Reverse Engineer/archive.json", "r", encoding="utf-8-sig") as f:
        return loads(f.read())


if __name__ == '__main__':
    S = Uploader()
    S.login(username, password)
    to_do = [
        (323, "4", "物語が始まる一歩", "A Step That Starts the Story"),
        (324, "4", "賑やかなお隣さん", "Lively Neighbor"),
        (325, "3", "さわっちゃダメ", "Don't Touch"),
        (326, "4", "イメトレinサーバー", "Image Training in the Server"),
        (327, "3", "なごみin公園", "Relaxing in the Park"),
        (328, "4", "物語（ウワサ）も知っている", "The Stories (Rumors) Also Know"),
        (329, "3", "そこに目を移して", "Look There"),
    ]
    pre_release = True
    if pre_release:
        for _id, rank, Jname, Ename in to_do:
            print(Ename + ";", end="")
            S.upload("Template:" + Ename.replace("?", "%3F"), template_format(_id, Ename, rank, Jname))
            S.upload(Ename.replace("?", "%3F"), format_text())
    else:
        coll = {}
        chars = get_chars()
        for piece in get_json()["pieceList"]:
            coll[piece["pieceId"] - 1000] = read(piece, chars)
        for _id, _, _, Ename in to_do:
            S.upload("Template:" + Ename.replace("?", "%3F"), template_format(_id, Ename, *coll[_id][1]))
            S.upload(Ename.replace("?", "%3F"), format_text(coll[_id][0].replace("＠", "<br />").replace("@", "<br />")))
            print(Ename)
    S.end()
