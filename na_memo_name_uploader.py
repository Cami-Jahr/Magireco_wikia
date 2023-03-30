from json import loads

from credentials import (
    password,
    username)
from helpers import get_memo_list
from upload_char import Uploader

with open("jsons/collection.json", "r", encoding="utf-8-sig") as f:
    json = loads(f.read())
    na_names = {}
    for item in json["pieceList"]:
        print(item)
        na_names[item["pieceId"]] = item["pieceName"]

names = get_memo_list()

for _id in names:
    try:
        print(names[_id], na_names[_id])
    except KeyError:
        print(names[_id], _id, "MISSING")

if __name__ == '__main__':
    S = Uploader()
    S.end()
    S.login(username, password)
    for _id in names:
        text = S.download_text("Template:" + names[_id])
        if "Naname" not in text:
            text = text.replace("Jname", "Naname = " + (na_names[_id] if _id in na_names else "") + "\n|Jname")
            S.upload("Template:" + names[_id], text)
    S.end()
