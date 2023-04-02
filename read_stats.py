import re
from collections import defaultdict
from json import loads

from effect_translator import (
    jp_to_en,
    remove_repeated_target,
    roman_to_full,
    translate,
    translate_jap_to_eng,
    translate_roman_to_ascii)
from helpers import get_char_list

textS = """{{Character/{{{1|Infobox}}}|{{{2|}}}|{{{3|}}}|{{{4|}}}|{{{5|}}}|{{{6|}}}|{{{7|}}}|{{{8|}}}|{{{9|}}}|{{{10|}}}|{{{11|}}}|{{{12|}}}|{{{13|}}}|{{{
14|}}}|{{{15|}}}|{{{16|}}}|{{{17|}}}|{{{18|}}}|{{{19|}}}"""
textM1 = """
| name = {0}
| name_jp = {1}
| name_na = 
| element = {7}
| base_rarity = {2}
| max_rarity = {3}
| id = {4}
| type = {9}
| growth_type = {11}
| school_jp = {6}
| voice_actor_jp = {8}
| designer_jp = {5}
| memoria = 
| release_date = {10}
| release_date_na = 
| event_limit = 
"""

textM2 = """
| accele_disks = {}
| blast_vert_disks = {}
| blast_hori_disks = {}
| charge_disks = {}
"""

textM3 = """
| 1star_hp_lv1 = {}
| 1star_attack_lv1 = {}
| 1star_defense_lv1 = {}
| 1star_hp_max = {}
| 1star_attack_max = {}
| 1star_defense_max = {}
| 1star_illustrator_jp = {}

| 2star_hp_lv1 = {}
| 2star_attack_lv1 = {}
| 2star_defense_lv1 = {}
| 2star_hp_max = {}
| 2star_attack_max = {}
| 2star_defense_max = {}
| 2star_illustrator_jp = {}

| 3star_hp_lv1 = {}
| 3star_attack_lv1 = {}
| 3star_defense_lv1 = {}
| 3star_hp_max = {}
| 3star_attack_max = {}
| 3star_defense_max = {}
| 3star_illustrator_jp = {}

| 4star_hp_lv1 = {}
| 4star_attack_lv1 = {}
| 4star_defense_lv1 = {}
| 4star_hp_max = {}
| 4star_attack_max = {}
| 4star_defense_max = {}
| 4star_illustrator_jp = {}

| 5star_hp_lv1 = {}
| 5star_attack_lv1 = {}
| 5star_defense_lv1 = {}
| 5star_hp_max = {}
| 5star_attack_max = {}
| 5star_defense_max = {}
| 5star_illustrator_jp = {}
"""

textE = "}}"

attributes = {
    "FIRE": "Flame",
    "TIMBER": "Forest",
    "DARK": "Dark",
    "LIGHT": "Light",
    "WATER": "Aqua",
    "VOID": "Void"
}

types = {
    "MAGIA": "Magia",
    "SUPPORT": "Support",
    "HEAL": "Heal",
    "BALANCE": "Balance",
    "ATTACK": "Attack",
    "DEFENSE": "Defense",
    "ULTIMATE": "Ultimate",
    "EXCEED": "Exceed",
    "ARUTEMETTO": "Ultimate",
    "AKUMA": "Akuma",
    "INFINITE": "Infinite",
}

star1 = [0, .05, .1, .15, .2, .25, .3, .35, .41, .46, .51, .56, .61, .66, .71, .76, .82, .87, .92, .97, 1.02, 1.07,
    1.12,
    1.17, 1.23, 1.28, 1.33, 1.38, 1.43, 1.48, 1.53, 1.58, 1.64, 1.69, 1.74, 1.79, 1.84, 1.89, 1.94, 2]
star2 = [0, .04, .08, .13, .17, .22, .26, .31, .35, .4, .44, .49, .53, .58, .62, .67, .71, .76, .8, .85, .89, .94, .98,
    1.03, 1.07, 1.12, 1.16, 1.21, 1.25, 1.3, 1.34, 1.39, 1.43, 1.48, 1.52, 1.57, 1.61, 1.66, 1.7, 1.75, 1.79, 1.84,
    1.88, 1.93, 1.97, 2.02, 2.06, 2.11, 2.15, 2.2]
star3 = [0, .04, .08, .12, .16, .2, .24, .28, .32, .36, .4, .44, .48, .52, .56, .61, .65, .69, .73, .77, .81, .85, .89,
    .93,
    .97, 1.01, 1.05, 1.09, 1.13, 1.17, 1.22, 1.26, 1.3, 1.34, 1.38, 1.42, 1.46, 1.5, 1.54, 1.58, 1.62, 1.66, 1.7,
    1.74,
    1.78, 1.83, 1.87, 1.91, 1.95, 1.99, 2.03, 2.07, 2.11, 2.15, 2.19, 2.23, 2.27, 2.31, 2.35, 2.4]
star4 = [0, .03, .06, .09, .13, .16, .19, .23, .26, .29, .32, .36, .39, .42, .46, .49, .52, .55, .59, .62, .65, .69,
    .72,
    .75, .78, .82, .85, .88, .92, .95, .98, 1.02, 1.05, 1.08, 1.11, 1.15, 1.18, 1.21, 1.25, 1.28, 1.31, 1.34, 1.38,
    1.41, 1.44, 1.48, 1.51, 1.54, 1.57, 1.61, 1.64, 1.67, 1.71, 1.74, 1.77, 1.81, 1.84, 1.87, 1.9, 1.94, 1.97, 2,
    2.04,
    2.07, 2.1, 2.13, 2.17, 2.2, 2.23, 2.27, 2.3, 2.33, 2.36, 2.4, 2.43, 2.46, 2.5, 2.53, 2.56, 2.6]
star5 = [0, .03, .06, .09, .12, .15, .18, .21, .24, .27, .3, .33, .36, .39, .42, .45, .48, .51, .54, .57, .6, .63, .66,
    .69,
    .72, .75, .78, .81, .84, .87, .9, .93, .96, 1, 1.03, 1.06, 1.09, 1.12, 1.15, 1.18, 1.21, 1.24, 1.27, 1.3, 1.33,
    1.36, 1.39, 1.42, 1.45, 1.48, 1.51, 1.54, 1.57, 1.6, 1.63, 1.66, 1.69, 1.72, 1.75, 1.78, 1.81, 1.84, 1.87, 1.9,
    1.93, 1.96, 2, 2.03, 2.06, 2.09, 2.12, 2.15, 2.18, 2.21, 2.24, 2.27, 2.3, 2.33, 2.36, 2.39, 2.42, 2.45, 2.48,
    2.51,
    2.54, 2.57, 2.6, 2.63, 2.66, 2.69, 2.72, 2.75, 2.78, 2.81, 2.84, 2.87, 2.9, 2.93, 2.96, 3]


def get_multiplier(rank, level):
    if rank == "RANK_1":
        return star1[level - 1]
    elif rank == "RANK_2":
        return star2[level - 1]
    elif rank == "RANK_3":
        return star3[level - 1]
    elif rank == "RANK_4":
        return star4[level - 1]
    elif rank == "RANK_5":
        return star5[level - 1]
    else:
        return 1


def calculate_growth_curve(_type):
    hp_mod = 1
    def_mod = 1
    atk_mod = 1
    if _type == "ATTACK":
        atk_mod = 1.03
        def_mod = .97
        hp_mod = .98
    elif _type == "DEFENSE":
        atk_mod = .98
        def_mod = 1.05
        hp_mod = .97
    elif _type == "HP":
        atk_mod = .97
        def_mod = .98
        hp_mod = 1.04
    elif _type == "ATKDEF":
        atk_mod = 1.02
        def_mod = 1.01
        hp_mod = .99
    elif _type == "ATKHP":
        atk_mod = 1.01
        def_mod = .99
        hp_mod = 1.02
    elif _type == "DEFHP":
        atk_mod = .99
        def_mod = 1.02
        hp_mod = 1.01
    return atk_mod, def_mod, hp_mod


def calculate_max(rank, _type, attack, defense, hp):
    e = get_multiplier("RANK_{}".format(rank), 0)
    atk_mod, def_mod, hp_mod = calculate_growth_curve(_type)
    return int(attack + attack * e * atk_mod), int(defense + defense * e * def_mod), int(hp + hp * e * hp_mod)


def calculate_min(rank, type, attack, defense, hp):
    e = get_multiplier("RANK_{}".format(rank), 0)
    g, h, k = calculate_growth_curve(type)
    _a = attack / (1 + (e * g))
    _d = defense / (1 + (e * h))
    _h = hp / (1 + (e * k))
    if _a % 1:
        _a = int(_a) + 1
    else:
        _a = int(_a)
    if _d % 1:
        _d = int(_d) + 1
    else:
        _d = int(_d)
    if _h % 1:
        _h = int(_h) + 1
    else:
        _h = int(_h)
    return _a, _d, _h


def print_min(rank, type, hp, attack, defense):
    a, d, h = calculate_min(rank, type, attack, defense, hp)
    return h, a, d


def print_max(rank, type, hp, attack, defense):
    a, d, h = calculate_max(rank, type, attack, defense, hp)
    return h, a, d


def format_info(_id):
    characters = get_char_list()
    with open("jsons/charaCard.json", "r", encoding="utf-8-sig") as f:
        info_dict = loads(f.read())
    work_on = None
    for dic in info_dict:
        if int(dic) == _id:
            work_on = info_dict[dic]
            break
    rank_stats = ["" for _ in range(5 * 8)]

    card = work_on["defaultCard"]
    low_rank = card["cardId"] % 10
    disk_layout = [card[f"commandType{i}"] for i in range(1, 6)]
    t3 = textM2.format(
        disk_layout.count('MPUP'), disk_layout.count('RANGE_V'), disk_layout.count('RANGE_H'),
        disk_layout.count('CHARGE'))
    rank = low_rank

    cards = ["defaultCard", *[f"evolutionCard{i}" for i in range(1, 5)]]
    for card in cards:
        try:
            rank = work_on[card]["cardId"] % 10
        except KeyError:
            break
        attack = work_on[card]["attack"]
        defence = work_on[card]["defense"]
        hp = work_on[card]["hp"]
        growth = work_on[card]["growthType"]
        try:
            illu = work_on[card]["illustrator"]
        except KeyError:
            illu = "-"
        try:
            atk_max, def_max, hp_max = calculate_max(rank, growth, attack, defence, hp)
            rank_stats[(rank - 1) * 7], rank_stats[((rank - 1) * 7) + 1], rank_stats[((rank - 1) * 7) + 2], rank_stats[
                ((rank - 1) * 7) + 3], rank_stats[((rank - 1) * 7) + 4], rank_stats[((rank - 1) * 7) + 5], rank_stats[
                ((rank - 1) * 7) + 6] = hp, attack, defence, hp_max, atk_max, def_max, illu
        except KeyError:
            print("Missing illustrator in eng or jap dict:", illu)
            raise SystemExit

    t5 = make_magia_doppel_and_connect(work_on, cards)

    t4 = textM3.format(*rank_stats)

    if _id == 1042:
        jap = "小さなキュゥべえ"
    else:
        try:
            jap = work_on["name"]
        except KeyError:
            jap = "UNKNOWN"
        try:
            jap += " (" + work_on["title"] + ")"
        except KeyError:
            pass

    att = attributes[work_on["attributeId"]]
    name = characters[_id].replace("_", " ")
    designer = work_on["designer"]
    school = work_on["school"]
    voice_actor = work_on["voiceActor"]
    try:
        type = types[work_on["initialType"]]
    except KeyError:
        try:
            type = "Cycles " + types[work_on["initialType"][7:]]  # Remove CIRCLE_
        except KeyError:
            type = "Unknown"
    try:
        release = work_on["openDate"][:10].replace("/", "-")
    except KeyError:
        release = "2017-08-22"
    try:
        t2 = textM1.format(
            name, jap, low_rank, rank, _id, designer, school, att, voice_actor,
            type, release, growth)
    except KeyError as e:
        print("Missing illustrator in eng or jap dict:", designer)
        raise e
    try:
        t1 = make_spirit_enchantment(work_on["enhancementCellList"])
    except KeyError:
        t1 = "\n\n"
    return textS + t2 + t3 + t4 + t1 + t5 + textE


def make_magia_doppel_and_connect(dic, cards):
    connect_name = magia_name = doppel_name = connect_icon = magia_icon = doppel_title = doppel_designer = ""
    all_connect_effects = defaultdict(int)
    all_megia_effects = defaultdict(int)
    all_doppel_effects = defaultdict(int)
    magia_scalings = {}
    connects = []
    magias = []
    for card in cards[::-1]:
        try:
            rank = dic[card]["cardId"] % 10
        except KeyError:
            continue
        connect = dic[card]["cardSkill"]
        connect_name = connect["name"]
        arts = []
        for i in range(1, 10):
            try:
                arts.append(connect[f"art{i}"])
            except KeyError:
                break
        connect_effects, connect_icon = translate(connect["shortDescription"], arts, True)
        for e in connect_effects:
            all_connect_effects[e] += 1
        connects.append(connect_effects)

        magia = dic[card]["cardMagia"]
        magia_name = magia["name"]
        arts = []
        for i in range(1, 10):
            try:
                arts.append(magia[f"art{i}"])
            except KeyError:
                break
        magia_effects, magia_icon = translate(magia["shortDescription"], arts, False)
        for e in magia_effects:
            magia_scalings[e] = "-" if magia_effects[e][2].replace("%", "").strip() == "0" else magia_effects[e][2]
            all_megia_effects[e] += 1
        magias.append(magia_effects)
        if rank == 5:
            doppel_arts = dic[card]["doppelCardMagia"]
            doppel_name = dic[card]["doppel"]["name"]
            doppel_title = dic[card]["doppel"]["title"]
            doppel_designer = dic[card]["doppel"]["designer"]
            arts = []
            for i in range(1, 10):
                try:
                    arts.append(doppel_arts[f"art{i}"])
                except KeyError:
                    break
            all_doppel_effects = translate(doppel_arts["shortDescription"], arts, False)[0]

    all_connect_effects = [e for e, i in sorted(all_connect_effects.items(), key=lambda x: x[1], reverse=True)]
    connect_effect_template = """| Connect effect {} = {}
"""
    connect_item_template = """| Connect {} / {} = {}
"""
    connect_string = """
| Connect name JP = {}
| Connect name EN = 
| Connect name NA = 
| Connect icon = {}
""".format(connect_name, connect_icon)
    for i in range(len(all_connect_effects)):
        connect_string += connect_effect_template.format(i + 1, all_connect_effects[i][:-1])
        for j in range(1, len(connects) + 1):
            try:
                word = connects[-j][all_connect_effects[i]]
                target = word[1].replace("Self / ", "").replace("Self", "").replace("1 Turn", "").strip()
                if not target:
                    st = word[0]
                elif word[0].replace("%", "").replace("0", "").strip() == "":
                    st = target
                else:
                    st = f"{target} / {word[0]}"
            except KeyError:
                st = "-"
            except IndexError:
                break
            connect_string += connect_item_template.format(i + 1, j, st)

    all_megia_effects = [e for e, i in sorted(all_megia_effects.items(), key=lambda x: x[1], reverse=True)]
    magia_effect_template = """| Magia effect {0} = {1}
| Magia scaling {0} = {2}
"""
    magia_item_template = """| Magia {} / {} = {}
"""
    magia_string = """
| Magia name JP = {}
| Magia name EN = 
| Magia name NA = 
| Magia icon = {}
""".format(magia_name, magia_icon)

    combine_similar_effects(all_megia_effects, magias, magia_scalings)
    for i in range(len(all_megia_effects)):
        magia_string += magia_effect_template.format(i + 1, all_megia_effects[i][:-1], magia_scalings[all_megia_effects[i]])
        for j in range(1, len(magias) + 1):
            try:
                word = magias[-j][all_megia_effects[i]]
                if word[1] == "1 Turn" or not word[1]:
                    st = word[0]
                elif word[0].replace("%", "").replace("0", "").strip() == "":
                    st = word[1]
                else:
                    st = f"{word[1]} / {word[0]}"
            except KeyError:
                st = "-"
            except IndexError:
                break
            magia_string += magia_item_template.format(i + 1, j, st)

    doppel_effect_template = """| Magia2 effect {0} = {1}
| Magia2 {0} = {2}
"""
    doppel_string = """
| Doppel Name = 
| Doppel Title = 
| Doppel Japanese Title = {}
| Doppel Shape = 
| Doppel Japanese Shape = {}
| Doppel Japanese Designer = {}
""".format(doppel_name, doppel_title, doppel_designer)
    i = 0
    for text, [effect, target_and_turns, scaling] in all_doppel_effects.items():
        i += 1
        effect_value = re.findall(r"[0-9.]+", effect)
        final_effect = effect
        if effect_value:
            scaling_value = re.findall(r"[0-9.]+", scaling)
            if scaling_value:
                final_value = float(effect_value[0]) + 4 * float(scaling_value[0])
                if final_value % 1 == 0:
                    final_value = str(int(final_value))
                else:
                    final_value = f"{final_value:.1f}"
                final_effect = effect.replace(effect_value[0], final_value)
        final_effect = target_and_turns + (" / " if target_and_turns and final_effect else "") + final_effect
        doppel_string += doppel_effect_template.format(i, text[:-1], final_effect)

    return connect_string + magia_string + doppel_string


def make_spirit_enchantment(cells):
    active_output = passive_output = ""
    accele_bonus = blast_bonus = charge_bonus = attack_bonus = defence_bonus = hp_bonus = 0
    passive_amount = active_amount = 1
    passive_template = """
| Passive {0} icon = {3}
| Passive {0} name = {2}
| Passive {0} name JP = {1}
| Passive {0} effect = {4}
"""
    active_template = """
| Active {0} icon = {3}
| Active {0} name = {2}
| Active {0} name JP = {1}
| Active {0} effect = {4}
| Active {0} cooldown = {5}
"""

    for cell in cells:
        if cell["enhancementType"] == "ATTACK":
            attack_bonus += cell["effectValue"]
        elif cell["enhancementType"] == "DEFENSE":
            defence_bonus += cell["effectValue"]
        elif cell["enhancementType"] == "HP":
            hp_bonus += cell["effectValue"]
        elif cell["enhancementType"] == "DISK_ACCELE":
            accele_bonus += cell["effectValue"]
        elif cell["enhancementType"] == "DISK_BLAST":
            blast_bonus += cell["effectValue"]
        elif cell["enhancementType"] == "DISK_CHARGE":
            charge_bonus += cell["effectValue"]
        elif cell["enhancementType"] == "SKILL":
            arts = []
            for i in range(1, 20):
                try:
                    arts.append(cell["emotionSkill"][f"art{i}"])
                except KeyError:
                    break
            eng_effect, icon = translate(cell["emotionSkill"]["shortDescription"], arts, True)
            remove_repeated_target(eng_effect)
            effect_output = ""
            for effect in eng_effect:
                if effect_output:
                    effect_output += " & "
                effect_output += effect[:-1]
                if eng_effect[effect][0]:
                    effect_output += f" [{eng_effect[effect][0]}]"
                if eng_effect[effect][1]:
                    effect_output += f" ({eng_effect[effect][1]})"

            skill_name_jp = cell["emotionSkill"]["name"].strip()
            skill_name_en = skill_name_jp
            skill_name_en = translate_jap_to_eng(skill_name_en)
            skill_name_en = translate_roman_to_ascii(skill_name_en)
            for c in skill_name_en:
                if ord(c) > 200:
                    print("missing translation?", repr(skill_name_en))
                    for c in skill_name_en:
                        print(ord(c), end=" ")
                    print()
                    break
            if cell["emotionSkill"]["type"] == "ABILITY":
                passive_output += passive_template.format(passive_amount, skill_name_jp, skill_name_en, icon, effect_output)
                passive_amount += 1
            else:  # SKILL
                try:
                    duration = cell["emotionSkill"]["intervalTurn"]
                except KeyError:
                    duration = "∞"
                active_output += active_template.format(active_amount, skill_name_jp, skill_name_en, icon, effect_output, duration)
                active_amount += 1
        elif cell["enhancementType"] == "START":
            pass
        else:
            print("\t\tUNKNOWN enhancementType:", cell["enhancementType"])

    # fill out so everyone has 13 passive and 1 active
    for i in range(passive_amount, 14):
        passive_output += passive_template.format(i, "", "", "", "")
    for i in range(active_amount, 2):
        active_output += active_template.format(1, "", "", "", "", "")

    accele_bonus //= 10
    blast_bonus //= 10
    charge_bonus //= 10
    if hp_bonus + attack_bonus + defence_bonus + accele_bonus + blast_bonus + charge_bonus == 0:
        accele_bonus = blast_bonus = charge_bonus = attack_bonus = defence_bonus = hp_bonus = ""
    stats = f"""
| se_hp_bonus = {hp_bonus}
| se_attack_bonus = {attack_bonus}
| se_defense_bonus = {defence_bonus}

| se accele bonus = {accele_bonus}
| se blast bonus = {blast_bonus}
| se charge bonus = {charge_bonus}
"""
    return stats + passive_output + active_output

def combine_similar_effects(all_megia_effects, magias, magia_scalings):
    """If e.g. Magia 1 / 3 has Def+ to Self while Magia 2/4 has Def+ to Allies this function combines them"""

    occurances_of_type = defaultdict(int)
    for eff in all_megia_effects:
        occurances_of_type[eff[:-1]] += 1
    to_combine = {}
    for effect_type, amount in occurances_of_type.items():
        if amount > 1:
            to_combine[effect_type] = []
            for rank_magia in magias:
                on_level_amount = 0
                for encoded_effect, atts in rank_magia.items():
                    if encoded_effect[:-1] == effect_type:
                        on_level_amount += 1
                to_combine[effect_type].append(on_level_amount)

    for effect_type, amount in to_combine.items():
        if all(nr < 2 for nr in amount):
            replacements = {}
            for eff in all_megia_effects:
                if eff[:-1] == effect_type:
                    new_eff = eff[:-1] + "X"
                    for rank_magia in magias:
                        if eff in rank_magia:
                            rank_magia[new_eff] = rank_magia[eff]
                            del rank_magia[eff]
                    replacements[eff] = new_eff
            for old_eff, new_eff in replacements.items():
                if new_eff not in all_megia_effects:
                    all_megia_effects[all_megia_effects.index(old_eff)] = new_eff
                else:
                    all_megia_effects.remove(old_eff)
                magia_scalings[new_eff] = magia_scalings[old_eff]
                del magia_scalings[old_eff]
