def get_char_list():
    di = get_list("chars.txt")
    del di[3052]  # Only have JP chars so removing Ashley
    return di

def get_memo_list():
    di = get_list("memoria_url_id.txt")
      # Only have JP memos so removing
    for id in (1464, 1485, 1487, 1498, 1500, 9001, 9002, 9003, 1502, 1503):
        del di[id]
    return di

def get_filenames():
    return get_list("gift_text.txt")

def get_list(li):
    names = {}
    with open(li) as f:
        for line in f.readlines():
            if line.strip():
                _id, name = line.strip().split(";")
                names[int(_id)] = name
    return names