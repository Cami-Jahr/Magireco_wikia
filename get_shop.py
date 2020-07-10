import urllib.request as ur
from json import loads

url1 = """https://android.magi-reco.com/magica/api/page/ShopTop?value=userFormationSheetList"""
request = ur.Request(url1,
                     headers={"f4s-client-ver": "2", "USER-ID-FBA9X88MAE": "0f47c009-0e45-4db8-ae9c-4eff18f6bf16"})
nshop = ur.urlopen(request).read().decode("utf-8")
with open("../../Reverse Engineer/shop.json", "r", encoding="utf-8-sig") as f:
    ns, os = loads(nshop)["shopList"], loads(f.read())["shopList"]
    for shop in ns:
        if shop not in os:
            _id = shop["shopId"]
            found = False
            for s in os:
                if _id == s["shopId"]:
                    found = True
                    print("New items:")
                    for item in shop["shopItemList"]:
                        if item not in s["shopItemList"]:
                            print(item)
                    print("\n\nOld items:")
                    for item in s["shopItemList"]:
                        if item not in shop["shopItemList"]:
                            print(item)
                    continue
            if not found:
                print(shop)

with open("../../Reverse Engineer/shop.json", "w", encoding="utf-8-sig") as f:
    f.write(ur.urlopen(request).read().decode("utf-8"))
