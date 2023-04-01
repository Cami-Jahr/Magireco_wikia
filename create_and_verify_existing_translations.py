import json


def check_duplicate(effect_name_jp, effect_name_en, translations, key, description):
    effect_name_jp = effect_name_jp.split("[")[0].strip()
    effect_name_en = effect_name_en.split("[")[0].strip()

    if effect_name_jp.strip() == "":
        return

    if effect_name_jp in translations:
        prev_key, prev_description, prev_effect_name = translations[effect_name_jp]
        if effect_name_en != prev_effect_name:
            print(
                f"Conflict between {prev_description} with id {prev_key} and {description} with id {key}\n\t{effect_name_jp}\n\t\t{effect_name_en}\n\t\t"
                f"{prev_effect_name}")
    else:
        translations[effect_name_jp] = (key, description, effect_name_en)


def create_effect_names():
    """To assure this is up-to-date run template_downloader.py#load_memos and template_downloader.py#load_girls first"""
    translations = {}

    with open("memos.json", "r", encoding="utf-8") as f:
        memos = json.load(f)
    for key, effect_name in memos['effect_name'].items():
        check_duplicate(memos['effect_name_JP'][key], effect_name, translations, key, "memo")

    with open("girls.json", "r", encoding="utf-8") as f:
        girls = json.load(f)

    wikia_translations_keys = [
        *[("Passive NR name".replace("NR", str(nr)), "Passive NR name JP".replace("NR", str(nr))) for nr in range(1, 20)],
        ("Active 1 name", "Active 1 name JP")
    ]

    for en, jp in wikia_translations_keys:
        for key, effect_name in girls[en].items():
            check_duplicate(girls[jp][key], effect_name, translations, key, "char")

    final_translations = {k: v[2] for k, v in translations.items()}  # Remove id from final list

    with open("existing_translations.json", "w", encoding="utf-8") as f:
        json.dump(final_translations, f, ensure_ascii=False)


create_effect_names()
