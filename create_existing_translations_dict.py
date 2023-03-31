import json


def create_effect_names():
    """To assure this is up-to-date run template_downloader.py#load_memos first"""

    with open("memos.json", "r", encoding="utf-8") as f:
        memos = json.load(f)

    translations = {}
    for key, effect_name in memos['effect_name'].items():
        effect_name_jp = memos['effect_name_JP'][key]
        if effect_name_jp.strip() == "":
            continue

        if effect_name_jp in translations:
            prev_key, prev_effect_name = translations[effect_name_jp]
            if effect_name != prev_effect_name:
                print(f"Conflict between id {key} and {prev_key} for {effect_name_jp}: {effect_name} -and- {prev_effect_name}")
        else:
            translations[effect_name_jp] = (key, effect_name)

    final_translations = {k: v[1] for k, v in translations.items()}  # Remove id from final list

    with open("existing_translations.json", "w", encoding="utf-8") as f:
        json.dump(final_translations, f, ensure_ascii=False)


create_effect_names()
