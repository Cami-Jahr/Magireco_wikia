from collections import defaultdict
from json import loads

char_list = {}
with open("chars.txt", "r", ) as f:
    for line in f.readlines():
        key, value, magia = line.strip().split(";")
        char_list[int(key)] = value


def get_char_list(item):
    return char_list[int(str(item)[:4])]


memo_list = {}
with open("memoria_url_id.txt", "r", ) as f:
    for line in f.readlines():
        _id, name = line.strip().split(";")
        memo_list[int(_id)] = name


def get_memo_list(item):
    return memo_list[int(str(item)[-3:])]


lookup_table = {}
with open("gift_text.txt", "r", encoding="utf-8") as f:
    for line in f.readlines():
        key, value, amount = line.strip().split(";")
        lookup_table[int(key)] = value


def get_gifts(item):
    return lookup_table[int(item)]


names = {
    "CURE_AP": "AP Potion",
    "CURE_AP_50": "AP Potion 50",
    "CURE_BP": "BP Potion",
    "GACHA_TICKET": "Gacha Ticket",
    "EVENT_BRANCH_1032_EXCHANGE_2": "Summer Exchange Ticket II",
    "PRISM": "Magia Chip",
}

atts = {
    "TIMBER": "Forest",
    "WATER": "Aqua",
    "LIGHT": "Light",
    "FIRE": "Flame",
    "ALL": "Master",
    "DARK": "Dark"
}


def get_item(item):
    if item[:4] == "HOME":
        return "Homescreen-" + item
    if item[:4] == "COMP":
        _names = item.split("_")
        return atts[_names[2]] + " Gem " + len(_names[3]) * "+"
    return names[item]


def formation(item):
    return "Formation" + item


def costume(item):
    return "Costume for " + char_list[int(str(item)[:4])]


items = {
    "RICHE_PACK": "CC",
    "GACHATICKET10_PACK": "10xGacha Ticket Pack",
    "GACHATICKET_PACK": "Gacha Ticket Pack",
    "AP_PACK_M": "Medium AP Pack",
    "AP_PACK_S": "Small AP Pack",
    "PRISM_SMALL_PACK": "3x Magia Chip",
}


def SET(item):
    if item[:5] == "EVENT":
        return "Event Item"
    return items[item]


def GEM(item):
    return char_list[int(item)]


types = {
    'GEM': GEM,
    'SET': SET,
    'LIVE2D': costume,
    'FORMATION_SHEET': formation,
    'ITEM': get_item,
    'PIECE': get_memo_list,
    'GIFT': get_gifts,
    'MAXPIECE': get_memo_list,
    'CARD': get_char_list
}


def read_shop():
    with open("jsons/shop.json", "r", encoding="utf-8-sig") as f:
        info_dict = loads(f.read())["shopList"]
    overview = {}
    for entry in info_dict:
        name = entry["name"]
        items = entry["shopItemList"]
        item_list = []
        for item in items:
            type = item["shopItemType"]
            description = types[type](item["genericId"])
            cost = item["needNumber"]
            try:
                limit = item["limitedNumber"]
            except KeyError:
                limit = " -"
            try:
                start = item["startAt"][:10]
            except KeyError:
                start = ""
            try:
                end = item["endAt"][:10]
            except KeyError:
                end = ""
            item_list.append([description, cost, limit, start, end])
        overview[name] = item_list
    return overview


def format_shop(shops):
    shops_list = sorted(shops.keys())
    store = defaultdict(list)
    for item in shops[shops_list[int(input("Index of wanted store of " + ", ".join(shops_list) + ": "))]]:
        store[item[-2] + "-" + item[-1]].append(item[:3])
    for periode, items in sorted(store.items()):
        if periode.count("/") != 2:
            stime, etime = periode.split("-")
            time = etime.split("/")
            if int(time[0]) < 2018 or int(time[1]) < 6:
                continue

        newline = False

        print("\n== Purchusable from " + periode[:-1] + " ==")
        print(
            """{| class="wikitable" style="width:100%; text-align:center"
            ! style="width:16.7%" |Item
            ! style="width:16.6%" |Quantity
            ! style="width:16.7%" |Price
            ! style="width:16.7%" |Item
            ! style="width:16.6%" |Quantity
            ! style="width:16.7%" |Price
            |-""")
        for item in items:
            print(
                """|{{ItemPic|size=50|item=%s}}
                |%s
                |%s x [[File:XXXXX.png|50px]]""" % (item[0], item[2], item[1]))
            if newline:
                print("|-")
            newline = not newline
        print("|}")


# user input based selection after listing

format_shop(read_shop())
