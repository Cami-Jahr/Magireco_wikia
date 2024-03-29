import os
from pathlib import Path

import read_awaken_mats as awaken
import read_stats
import read_trivia as story
import read_voice_text as voice
from helpers import (
    get_char_list,
    get_filenames)
from wikibot import wikibot

galley_base = """<tabber>
Memoria=
{{MemoriaGallery}}
|-|Videos=
{{Videos}}
</tabber>
"""

costume_base = """<tabber>
Magical Girl = 
</tabber>
"""

trivia_base = """==[[Magia Archive]] Profile==
''Not yet featured in Magia Archive.''
<!--*Hometown:
*Age: 
*Height:
*Weapon:
*Ability:
*Soul Gem Location:-->
{{SideStory
|Side Story Translation Link = 
|Side Story = 
}}"""


def upgrades_section(char_name: str):
    return "{{" + f"{char_name.replace('_', ' ')} Items|Items" + "}}"


def main_section(char_name: str, text: str):
    return "{{" + char_name + "}}" + "\n\n{{Description\n| en = \n| jp = " + text + "\n}}\n\n{{Tabs}}"


def abilities_section(char_name: str, doppel_story: str):
    text = "{{" + char_name + "|Abilities}}"
    if doppel_story and doppel_story != 'ー':
        text += "\n\n{{Description\n| en = \n| jp = " + doppel_story + "\n}}"
    return text


upload_new_files = False
refresh_local_files = True

if __name__ == '__main__':
    files = get_filenames()
    chars = get_char_list()
    c_list = sorted(list(chars))

    mat_list = awaken.read_mats_json()
    formatted_mats = awaken.mats_formater(mat_list, files, chars)
    voice_lines = voice.read_lines_json()
    formatted_voice = voice.mats_sender(voice_lines)
    trivia = story.read_trivia_json()
    formatted_trivia = story.story_formater(trivia)
    main_parent = os.path.join("wikia_pages", "characters")

    for i in reversed(c_list):
        ch = chars[i].replace(" ", "_")
        print(ch)
        parent = os.path.join(main_parent, ch)
        Path(parent).mkdir(parents=True, exist_ok=True)

        main_temp_text, main_page_text = read_stats.format_info(i), main_section(ch, formatted_trivia[i][0])
        ability_page_text = abilities_section(ch, formatted_trivia[i][1])
        upgrade_temp_text = formatted_mats[i]
        upgrade_page_text = upgrades_section(ch)
        voice_page_text = formatted_voice[i]

        for page, text in (
                (f"Template:{ch}", main_temp_text),
                (f"Template:{ch}_Items", upgrade_temp_text),
                (f"{ch}", main_page_text),
                (f"{ch}/Abilities", ability_page_text),
                (f"{ch}/Upgrades", upgrade_page_text),
                (f"{ch}/Trivia", trivia_base),
                (f"{ch}/Costumes", costume_base),
                (f"{ch}/Gallery", galley_base),
                (f"{ch}/Quotes", voice_page_text)):

            if refresh_local_files:
                local_file = page.replace(":", "-").replace("/", "-")
                with open(os.path.join(parent, local_file + ".txt"), "w", encoding="utf-8-sig") as f:
                    f.write(text)

            if upload_new_files:
                online_text = wikibot.download_text(page)
                if len(online_text) < 5:  # Only upload new files, aka replace files without length
                    wikibot.upload(page, text)

