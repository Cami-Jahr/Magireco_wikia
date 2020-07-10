from json import loads


def read_trivia_json():
    with open("jsons/charaCard.json", "r", encoding="utf-8-sig") as f:
        info_dict = loads(f.read())
    overview = {}
    for entry in info_dict:
        temp = [info_dict[entry]["description"].replace("＠", "<br />")]
        try:
            idx = 0
            for i in range(5, 0, -1):
                if f"evolutionCardId{i}" in info_dict[entry] and info_dict[entry][f"evolutionCardId{i}"] % 10 == 5:
                    idx = i
                    break
            temp.append(info_dict[entry][f"evolutionCard{idx}"]["doppel"]["description"].replace("＠", "<br />"))
        except KeyError:
            temp.append("")
        overview[int(entry)] = temp
    return overview


def story_formater(story_list):
    overview = {}
    for _id, stry in story_list.items():
        overview[_id] = stry
    return overview
