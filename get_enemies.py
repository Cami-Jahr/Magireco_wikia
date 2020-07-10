import urllib.request as ur

url1 = """https://ios.magi-reco.com/magica/api/page/EnemyCollection"""
request = ur.Request(url1,
                     headers={"f4s-client-ver": "2", "USER-ID-FBA9X88MAE": "6e509c61-3639-450f-b250-b7ebbc90d67d"})

content = ur.urlopen(request).read().decode("utf-8")
with open("../../Reverse Engineer/archive_enemies.json", "w", encoding="utf-8-sig") as f:
    f.write(content)
print(content)
