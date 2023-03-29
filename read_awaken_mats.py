from json import loads


def read_awaken(entry):
    awakening_mats = []
    max_rank = 0
    cards = ["defaultCard", *[f"evolutionCard{i}" for i in range(1, 5)]]
    for card in cards:
        try:
            mats_location = entry[card]["cardCustomize"]
        except KeyError:
            break
        mats = []
        max_rank = entry[card]["cardId"] % 10
        for i in range(1, 7):
            try:
                mats.append((mats_location["giftId{}".format(i)], mats_location["giftNum{}".format(i)],
                                mats_location["bonusCode{}".format(i)],
                                mats_location["bonusNum{}".format(i)] // 10))
            except KeyError:
                pass
        awakening_mats.append(mats)
    return max_rank, awakening_mats


def read_magia(entry):
    a = []
    b = []
    for line in entry:
        if line[-7:-1] == "GiftId":
            a.append(line)
        elif line[-8:-1] == "GiftNum":
            b.append(line)
    magia_mats = []
    for aline in sorted(a):
        if aline[:4] == "firs":
            number = 1
        elif aline[:4] == "seco":
            number = 2
        elif aline[:4] == "thir":
            number = 3
        else:
            number = 4
        for bline in b:
            if aline[:4] == bline[:4] and aline[-1] == bline[-1]:
                magia_mats.append((number, int(aline[-1]), entry[aline], entry[bline]))
    return magia_mats


def read_mats_json():
    with open("jsons/charaCard.json", "r", encoding="utf-8-sig") as f:
        info_dict = loads(f.read())
    overview = []
    for entry in info_dict:
        magia = read_magia(info_dict[entry])
        rank, awaken = read_awaken(info_dict[entry])
        overview.append((int(entry), rank, magia, awaken))
    return overview


def mats_formater(mat_list, file_names, char_list):
    overview = {}
    for entry in mat_list:
        _id, max_rank, magia_mats, awaken_mats = entry
        magia_string = """{{Character/{{{1|Items}}}|{{{2|}}}|{{{3|}}}|{{{4|}}}|{{{5|}}}|{{{6|}}}|{{{7|}}}|{{{8|}}}|{{{9|}}}|{{{10|}}}|{{{11|}}}|{{{12|}}}|{{{13|}}}|{{{14|}}}|{{{15|}}}|{{{16|}}}|{{{17|}}}|{{{18|}}}|{{{19|}}}|{{{20|}}}|{{{21|}}}|{{{22|}}}|{{{23|}}}|{{{24|}}}|{{{25|}}}|{{{26|}}}|{{{27|}}}|{{{28|}}}|{{{29|}}}|{{{30|}}}"""
        try:
            magia_string += """\n|name = {}""".format(char_list[_id])
        except KeyError:
            print(f"MISSING CHARACTER NAME IN CHARS.TXT FOR ID={_id}")
            continue
        old_rank = 0
        for mat in magia_mats:
            if old_rank != mat[0] + 1:
                old_rank = mat[0] + 1
                magia_string += "\n"
            magia_string += """|Magia Item {0}/{1} = {2}
|Magia quantity {0}/{1} = {3}
""".format(mat[0] + 1, mat[1], file_names[mat[2]], mat[3])

        awaken_string = "\n"
        final = len(awaken_mats)
        for level in range(len(awaken_mats)):
            for bonus in awaken_mats[level]:
                lvl = level + 1
                json_poss = {"ATTACK": 2, "DEFENSE": 3, "HP": 1, "ACCEL": 6, "BLAST": 4, "CHARGE": 5}
                poss_wiki = {2: "ATK", 3: "DEF", 1: "HP", 6: "Accele", 4: "Blast", 5: "Charge"}
                awaken_string += """|Item{0}{1} = {2}
|Quantity{0}{1} = {3}
|Buff{4}{0} = {5}
""".format(lvl, json_poss[
                    bonus[2]], file_names[bonus[0]], bonus[1], poss_wiki[json_poss[bonus[2]]], bonus[3])
            awaken_string += "\n"
        cost = {4: "1000000", 3: "300000", 2: "100000", 1: "10000"}
        for i in range(1, final):
            awaken_string += "|QuantityCC{} = {}\n".format(i, cost[max_rank - final + i])
        awaken_string += "}}"
        overview[_id] = (magia_string + "\n" + awaken_string)
    return overview
