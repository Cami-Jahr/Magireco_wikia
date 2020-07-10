#from upload_char import Uploader
#from credentials import username, password
#import re

"""
S = Uploader()
S.login(username, password)

with open("chars.txt", "r", ) as f:
    for line in f.readlines():
        _id, name = line.strip().split(";")
        for st in ("", "/Abilities"):
            text = S.download_text(name + st)
            desc = re.findall(r" " "\{\{Description.*?\|(.*?)}}" " ", text, re.DOTALL)[0]
            if desc:                
                descs = re.findall(r" " "(.*?)=(.*?)(\||$)" " ", desc, re.DOTALL)
                n_descs = []
                for lang, des, _ in descs:
                    text = text.replace(des, des.strip().replace("\n", "<br>"))
                text = text.replace("\n|", "|").replace("|", "\n|")
                text = text.replace(" = ", "=").replace(" =", "=").replace("= ", "=").replace("=", " = ")
                S.upload(name + st, text)
S.end()
"""

L = []
with open("div.txt") as f:
    for line in f.readlines():
        line = line.strip()
        L.append(line + " ")
        if "Japanese" in line:
            try:
                line = line[:line.index("= ") + 1]
            except ValueError:
                pass
            L.append(line.replace("Japanese", "NA") + " ")
        
print("\n".join(L))
with open("div.txt", "w") as f:
    f.write("\n".join(L))