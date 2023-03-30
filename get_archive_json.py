import urllib.request as ur

url1 = """https://ios.magi-reco.com/magica/api/page/CharaCollection?value=\
pieceList,giftList,user,gameUser,itemList"""
# mirrors url1 = """https://ios.magi-reco.com/magica/api/page/EventArenaRankingTop"""
request = ur.Request(
    url1,
    headers={"f4s-client-ver": "2", "USER-ID-FBA9X88MAE": "0f47c009-0e45-4db8-ae9c-4eff18f6bf16"})

with open("../../Reverse Engineer/archive.json", "w", encoding="utf-8-sig") as f:
    f.write(ur.urlopen(request).read().decode("utf-8"))
print(ur.urlopen(request).read().decode("utf-8"))
