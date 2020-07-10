from json import loads


def read_designer_json(char_names, eng_name):
    with open("/jsons/charaCard.json", "r", encoding="utf-8") as f:
        info_dict = loads(f.read())["charaList"]
    overview = {}
    for entry in info_dict:
        designer = entry["chara"]["designer"]
        try:
            designer = designer[0], char_names[designer[0]], designer[1], eng_name[designer[1]]
        except KeyError:
            designer = designer[0], char_names[designer[0]], "", designer[1]
        overview[int(entry)] = designer
    return overview
