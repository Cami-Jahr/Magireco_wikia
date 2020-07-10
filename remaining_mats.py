import read_awaken_mats
from collections import defaultdict
from helpers import get_char_list, get_filenames

cc_cost = {
    -1: 1410000,
    0: 1410000,
    1: 1400000,
    2: 1300000,
    3: 1000000,
    4: 0,
}

def main(owned=True, dont_show_done=True):
    files = get_filenames()
    files[0] = ("CC", 7700000)
    chars = get_char_list()
    mat_list = read_awaken_mats.read_mats_json()
    counter = defaultdict(int)
    for _id, rank, magia, awaken in mat_list:
        current_rank = chars[_id]
        if owned:
            if current_rank != -1:
                counter[0] += cc_cost[current_rank]
        else:
            counter[0] += cc_cost[current_rank]
        for item_rank, slot, code, amount in magia:
            if owned:
                if item_rank > current_rank > 0:
                    counter[code] += amount
            else:
                if item_rank > current_rank:
                    counter[code] += amount

    length = len(max([files[i][0] for i in counter.keys()], key=len))
    for code, amount in sorted(counter.items()):
        name, have = files[code]
        if (dont_show_done and amount - have > 0) or not dont_show_done:
            print("{:<{}}: {:<,}".format(name, length, amount - have))


if __name__ == '__main__':
    main(owned=True, dont_show_done=True)
