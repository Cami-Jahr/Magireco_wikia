from json import loads


def read_other(entry):
    illu = []
    for card in entry["cardList"]:
        try:
            illu.append(card["card"]["illustrator"])
        except KeyError:
            illu.append(None)
    return illu


def read_illustrator_json():
    with open("/jsons/charaCard.json", "r", encoding="utf-8") as f:
        info_dict = loads(f.read())["charaList"]
    overview = []
    for entry in info_dict:
        illu = [int(entry), *read_other(entry)]
        overview.append(illu)
    return overview
