import re
from wikibot import wikibot

filtered_pages = {"[[Enemies]]", }
filtered_characters = {"Rumor Tsuruno", "Rumor of the Ten-Thousand-Year Sakura", "Rumor Sana"}


def print_occurrences():
    x = 0
    page = wikibot.download_text("Enemies")
    enemies = re.findall(r"""\{\{ItemPic\|size=100\|item=(.*?)}}""", page)
    for enemy in set(enemies) - filtered_characters:
        x += 1
        pages = sorted(set([p.title(with_ns=False, as_link=True) for p in wikibot.image_usage(enemy + ".png", namespaces=0)]) - filtered_pages)

        output = "\n\n==Appearances/Encounters=="
        old_text = wikibot.download_text(enemy)
        base_text = old_text.split(output)[0]
        for occurrence in pages:
            output += "\n* " + occurrence
        final_text = base_text + output
        wikibot.upload(enemy, final_text)


print_occurrences()
