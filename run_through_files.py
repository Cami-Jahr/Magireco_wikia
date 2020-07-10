import urllib.request as ur
import re

with open("chars.txt") as f:
    for l in f.readlines():
        name = l.split(";")[1].strip().replace(" ", "_")
        url1 = f"""https://magireco.fandom.com/wiki/{name}/Abilities?action=edit"""
        request = ur.Request(url1)

        try:
            box = re.findall(r"""<textarea.*?name="wpTextbox1">(.*?)</textarea>""", ur.urlopen(request).read().decode("utf-8"), re.DOTALL)[0]
            desc = re.findall(r"""\{\{Description.*?\|(.*?)}}""", box, re.DOTALL)[0]
            descs = re.findall(r"""(.*?)=(.*?)(\||$)""", desc, re.DOTALL)
            for lang, des, _ in descs:
                if ">&lt;" in des:
                    print(url1)
                    break
                
        except IndexError:
            pass
        except:
            print(url1)