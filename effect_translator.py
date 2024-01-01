import json
import re

from helpers import get_char_list

girls = get_char_list()

roman_to_full = {
    "Ⅰ": "I",
    "Ⅱ": "II",
    "Ⅲ": "III",
    "Ⅳ": "IV",
    "Ⅴ": "V",
    "Ⅵ": "VI",
    "Ⅶ": "VII",
    "Ⅷ": "VIII",
    "Ⅸ": "IX",
    "X": "X",
    "Ⅹ": "X",
    "XI": "XI",
    "XⅠ": "XI",
    "XII": "XII",
    "XIII": "XIII",
    "XⅡ": "XII",
    "XⅢ": "XIII",
    "ⅩⅢ": "XIII",
    "XIV": "XIV",
    "XV": "XV",
    "XⅤ": "XV",
    "XVI": "XVI",
    "XVII": "XVII",
    "XⅧ": "XVII",
    "XVIII": "XVIII",
    "XⅧ": "XVIII",
    "XIX": "XIX",
    "XX": "XX",
    "XXI": "XXI",
    "XXII": "XXII",
    "XXIII": "XXIII",
    "XXIV": "XXIV",
    "XXV": "XXV",
    "8": "8",  # ‘Tis I, the Third Amane Sister, Tsukune
    "88": "88",
}


def translate_roman_to_ascii(string):
    for roman_nr, latin_nr in roman_to_full.items():
        string = string.replace(roman_nr, latin_nr)
    return string


# Format is (description, uses_roman, does_not_state_target)

good = {
    "AUTO_HEAL": ("Regenerate HP", True, False),
    "PURSUE": ("Chase", True, False),
    "AVOID": ("Evade", True, False),
    "DAMAGE_DOWN": ("Damage Cut", True, False),
    "PROVOKE": ("Provoke", True, False),
    "GUTS": ("Endure", False, False),
    "MP_PLUS_WEAKED": ("MP Up When Attacked By Weak Element", True, False),
    "DAMAGE_DOWN_BLAST": ("Blast Damage Cut", True, False),
    "CRITICAL": ("Critical Hit", True, False),
    "PROTECT": ("Guardian", True, True),
    "DEFENSE_IGNORED": ("Defense Pierce", True, False),
    "SKILL_QUICK": ("Skill Quicken", True, False),
    "COUNTER": ("Counter", True, False),
    "DAMAGE_DOWN_ACCEL": ("Accele Damage Cut", True, False),
    "DAMAGE_DOWN_NODISK": ("Magia Damage Cut", True, False),
    "DAMAGE_DOWN_FIRE": ("Flame Attribute Damage Cut", True, False),
    "DAMAGE_DOWN_TIMBER": ("Forest Attribute Damage Cut", True, False),
    "DAMAGE_DOWN_DARK": ("Dark Attribute Damage Cut", True, False),
    "DAMAGE_DOWN_LIGHT": ("Light Attribute Damage Cut", True, False),
    "DAMAGE_DOWN_WATER": ("Aqua Attribute Damage Cut", True, False),
    "DAMAGE_DOWN_VOID": ("Void Attribute Damage Cut", True, False),
    "C_COMBO_PLUS": ("Charge Combo Charge Count Up", False, False),
    "MP_PLUS_DAMAGED": ("MP Up When Damaged", True, False),
    "DAMAGE_UP_BAD": ("Damage Up Versus Enemies Affected With Status Ailments", True, False),
    "SURVIVE": ("Survive", True, False),
    "MP_PLUS_BLAST": ("Blast MP Gain Up", True, False),
    "DAMAGE_UP": ("Damage Increase", True, False),
    "ATTACK_UP": ("Attack Up", True, False),
    "IMITATE_ATTRIBUTE": ("Variable", True, False),
    "NO_COST_CHARGE": ("Charge Conservation", True, False),
    "BARRIER": ("Barrier", True, False),
    "REFLECT_DEBUFF": ("Reflect Debuffs", True, False),
}

bad = {
    "CHARM": ("Charm", True, False),
    "POISON": ("Poison", True, False),
    "FOG": ("Fog", True, False),
    "CURSE": ("Curse", True, False),
    "BURN": ("Burn", True, False),
    "STUN": ("Stun", True, False),
    "BLINDNESS": ("Dazzle", True, False),
    "DARKNESS": ("Darkness", True, False),
    "BAN_SKILL": ("Skill Seal", True, False),
    "BAN_MAGIA": ("Magia Seal", True, False),
    "RESTRAINT": ("Bind", True, False),
    "DAMAGE_UP_BAD_NUM": ("Frailty", True, False),
}

enchant = {
    "CHARM": ("Charm on Attack", True, True),
    "STUN": ("Stun on Attack", True, True),
    "POISON": ("Poison on Attack", True, True),
    "FOG": ("Fog on Attack", True, True),
    "BLINDNESS": ("Dazzle on Attack", True, True),
    "CURSE": ("Curse on Attack", True, True),
    "BURN": ("Burn on Attack", True, True),
    "DARKNESS": ("Darkness on Attack", True, True),
    "RESTRAINT": ("Bind on Attack", True, True),
    "BAN_SKILL": ("Skill Seal on Attack", True, True),
    "BAN_MAGIA": ("Magia Seal on Attack", True, True),
}

buff = {
    "MAGIA": ("Magia Damage Up", True, False),
    "MP_GAIN_OVER100": ("MP Gain Up When Over 100 MP", True, False),
    "DOPPEL": ("Doppel Damage Up", True, False),
    "ACCEL": ("Accele MP Gain Up", True, False),
    "BLAST": ("Blast Damage Up", True, False),
    "DEFENSE": ("Defense Up", True, False),
    "RESIST": ("Status Ailment Resistance Up", True, False),
    "MP_GAIN": ("MP Gain Up", True, False),
    "CHARGE": ("Charged Attack Damage Up", True, False),
    "CHARGING": ("Charge Disc Damage Up", True, False),
    "ATTACK": ("Attack Up", True, False),
    "ATTACK_DARK": ("Dark Attribute Attack Up", True, False),
    "ATTACK_FIRE": ("Flame Attribute Attack Up", True, False),
    "ATTACK_WATER": ("Aqua Attribute Attack Up", True, False),
    "ATTACK_TIMBER": ("Forest Attribute Attack Up", True, False),
    "ATTACK_LIGHT": ("Light Attribute Attack Up", True, False),
    "DAMAGE": ("Damage Up", True, False),
}

ignore = {
    "BAN_SKILL": ("Anti-Skill Seal", True, False),
    "BAN_MAGIA": ("Anti-Magia Seal", True, False),
    "AVOID": ("Anti-Evade", True, False),
    "DEBUFF": ("Anti-Debuff", False, False),
    "COUNTER": ("Anti-Counter", True, False),
    "DAMAGE_DOWN": ("Ignore Damage Cut", True, False),
    "POISON": ("Anti-Poison", True, False),
    "CURSE": ("Anti-Curse", True, False),
    "CHARM": ("Anti-Charm", True, False),
    "BURN": ("Anti-Burn", True, False),
    "RESTRAINT": ("Anti-Bind", True, False),
    "PROVOKE": ("Anti-Provoke", True, False),
    "STUN": ("Anti-Stun", True, False),
    "FOG": ("Anti-Fog", True, False),
    "BLINDNESS": ("Anti-Dazzle", True, False),
    "DARKNESS": ("Anti-Darkness", True, False),
    "CRITICAL": ("Negate Critical Hit", True, False),
    "CONDITION_BAD": ("Negate Status Ailments", True, False),
}

revoke = {
    "BAD": ("Remove Status Ailments", False, False),
    "GOOD": ("Remove Granted Effects", False, False),
    "BUFF": ("Remove Buffs", False, False),
    "DEBUFF": ("Remove Debuffs", False, False),
}

buff_party_die = {
    "ATTACK": ("Attack Up When Ally Dies", True, False),
    "DEFENSE": ("Defense Up When Ally Dies", True, False),
}

buff_dying = {
    "ATTACK": ("Attack Up When At Critical Health", True, False),
    "DEFENSE": ("Defense Up When At Critical Health", True, False),
}

initial = {
    "MP": ("MP Gauge Increased On Battle Start", False, False),
}

heal = {
    "MP_DAMAGE": ("MP Damage", True, False),
    "HP": ("HP Restore", True, False),
    "MP": ("MP Restore", True, False),
}

debuff = {
    "DEFENSE": ("Defense Down", True, False),
    "ATTACK": ("Attack Down", True, False),
    "DAMAGE": ("Damage Down", True, False),
    "WEAK_FIRE": ("Flame Attribute Resistance Down", True, False),
    "WEAK_TIMBER": ("Forest Attribute Resistance Down", True, False),
    "WEAK_DARK": ("Dark Attribute Resistance Down", True, False),
    "WEAK_LIGHT": ("Light Attribute Resistance Down", True, False),
    "WEAK_WATER": ("Aqua Attribute Resistance Down", True, False),
    "WEAK_VOID": ("Void Attribute Resistance Down", True, False),
    "WEAK_CHARGE_DONE": ("Charged Attack Received Damage Up", True, False),
    "WEAK_BLAST": ("Blast Disc Received Damage Up", True, False),
    "MP_GAIN": ("MP Gain Down", True, False),
    "RESIST": ("Status Ailment Resistance Down", True, False),
    "MAGIA": ("Magia Damage Down", True, False),
    "ACCEL": ("Accele MP Gain Down", True, False),
    "BLAST": ("Blast Damage Down", True, False),
    "CHARGE": ("Charged Attack Damage Down", True, False),
    "ADD_DAMAGE": ("Apply Extra Damage", True, False)
}

buff_hpmax = {
    "ATTACK": ("Attack Up While At Max Health", True, False),
    "DEFENSE": ("Defense Up While At Max Health", True, False),
}

draw = {
    "AGAIN": ("Redraw Discs", False, False),
    "ACCEL": ("Accele Draw", False, False),
    "BLAST": ("Blast Draw", False, False),
    "CHARGE": ("Charge Draw", False, False),
    "ALIGNMENT": ("Attribute Draw", False, False),
    "SELF": ("Monopolize Draw", False, False),
}

limited = {
    "DAMAGE_UP": ("Damage Up Versus Witches", True, False),
}

attack = {
    "ALL": ("Damage All Enemies", True, True),
    "TARGET": ("Damage One Enemy", True, True),
    "HORIZONTAL": ("Damage A Horizontal Line", True, True),
    "VERTICAL": ("Damage A Vertical Line", True, True),
    "RANDOM1": ("Damage a Random Enemy", True, True),
    "RANDOM2": ("Damage 2 Random Enemies", True, True),
    "RANDOM3": ("Damage 3 Random Enemies", True, True),
    "RANDOM4": ("Damage 4 Random Enemies", True, True),
    "RANDOM5": ("Damage 5 Random Enemies", True, True),
}

resurrect = {
    "ONE": ("Revive one Ally", False, False),
}

buff_die = {
    "ATTACK": ("Attack Up Upon Death", True, True),
    "DEFENSE": ("Defense Up Upon Death", True, True),
}

other = {
    "QUESTBATTLE_ATK": ("((Increased ATK during some quest))", False, False),
    "QUESTBATTLE_DEF": ("((Increased DEF during some quest))", False, False),
    "EPISODE_UP": ("Episode Experience Gain Increased", True, False),
    "GOLD_UP": ("CC Gain Up", True, False),
}

damage = {
    "ALLY": ("Receive Damage", False, False),
}

allies = {
    "BUFF": ("Extend Buffs", True, False),
}

enemies = {
    "DEBUFF": ("Extend Debuffs", True, False),
}

master = {  # verbCode
    "CONDITION_GOOD": good,
    "CONDITION_BAD": bad,
    "BUFF": buff,
    "IGNORE": ignore,
    "REVOKE": revoke,
    "ENCHANT": enchant,
    "BUFF_PARTY_DIE": buff_party_die,
    "BUFF_DYING": buff_dying,
    "INITIAL": initial,
    "HEAL": heal,
    "DEBUFF": debuff,
    "BUFF_HPMAX": buff_hpmax,
    "DRAW": draw,
    "LIMITED_ENEMY_TYPE": limited,
    "ATTACK": attack,
    "RESURRECT": resurrect,
    "BUFF_DIE": buff_die,
    "OTHER": other,
    "DAMAGE": damage,
    "TURN_ALLY": allies,
    "TURN_ENEMY": enemies,
}

# Hard coded first before ・, general tls after
jp_to_en = {
    "受け継ぎし加護": "Inherited Protection",
    "ヘルスリカバリー": "Health Recovery",
    "MPブースト": "MP Boost",
    "フルスウィングアップ": "Full Swing Up",
    "イグノアデバフ": "Ignore Debuffs",
    "グリッターライズ": "Glitter Rise",
    "フルスウィング": "Full Swing Up",
    "クライシスブルーム": "Crisis Bloom",
    "スキルクイック": "Skill Quicken",
    "フルバースト": "Full Burst",
    "ピースフルカーム": "Peaceful Calm",
    "アタックライズ": "Attack Rise",
    "ブルームライズ": "Bloom Rise",
    "アクセルライズ": "Accelerise",
    "フレッシュヒール": "Fresh Heal",
    "ブラストサルテーション": "Blast Salutation",
    "エンチャントシールド": "Enchantment Shield",
    "アンチデバフ": "Anti-Debuff",
    "アディクトキラー": "Addict Killer",
    "バトルセンス": "Battle Sense",
    "イグノアデバフ・サークル": "Ignore Debuff Circle",
    "アクセルフォースアデプト": "Accele Force Adept",
    "コンセントレイト": "Concentrate",
    "ディスクシャッフル": "Disc Shuffle",
    "クロスカウンター": "Cross Counter",
    "ダークシールド": "Dark Shield",
    "チャージエキスパート": "Charge Expert",
    "アクアフォール": "Aqua Fall",
    "クライシスブルー": "Crisis Bloom",
    "インスパイアドステップ": "Inspired Step",
    "マナスプリング": "Mana Spring",
    "ソリッドライズ": "Solid Rise",
    "カーススクリーム": "Curse Scream",
    "チャージコンボプラス": "Charge Combo Plus",
    "クライシスアタック": "Crisis Attack",
    "アップリフト": "Uplift",
    "クライシスガード": "Crisis Guard",
    "ブルームダウン": "Bloom Down",
    "アタックダウン": "Attack Down",
    "レジストダウン": "Resist Down",
    "ガードライズ・サークル": "Guard Rise Circle",
    "パンプアップ": "Pump Up",
    "エンスジアスティカリー": "Enthusiastically",
    "マナアブソーブ": "Mana Absorb",
    "チアアップ": "Cheer Up",
    "フルゲージドライブ": "Full Gauge Drive",
    "タイムスキップ": "Time Skip",
    "ホークアイ": "Hawkeye",
    "シールドアピール": "Shield Appeal",
    "リーンホース": "Reinforce",
    "ハウリングロアー": "Howling Roar",
    "リムーブスペル": "Remove Spell",
    "ダークフォール": "Dark Fall",
    "ファーストエイド": "First Aid",
    "テンペスト": "Tempest",
    "無限大の可能性": "Infinite Possibilities",
    "アクアアサルト": "Aqua Assault",
    "フレイムグリッター": "Flame Glitter",
    "ウェポンブラスト": "Weapon Blast",
    "バーサク・ライズ": "Berserk Rise",
    "ライトライズ": "Light Rise",
    "ライトブレイク": "Light Break",
    "ソリッド ディフェンス": "Solid Defense",
    "スターブレイカー": "Star Breaker",
    "エターナルラヴ": "Eternal Love",
    "ディスアーマメント": "Disarmament",
    "オブリビオン": "Oblivion",
    "ジアンサー": "The Answer",
    "バタリングラム": "Battering Ram",
    "アンチ": "Anti",
    "・": " ",
    "[": " [",
    "ブレス": "Brace",
    "サークル": "Circle",
    "エリミネイト": "Eliminate",
    "アップ": " Up",
    "インビジブル": "Invisible",
    "ライジング": "Rising",
    "ストローク": "Stroke",
    "ポゼッション": "Possesion",
    "アナライズ": "Analyze",
    "スラッシュ": "Slash",
    "ミスチーフ": "Mischief",
    "フラッシュ": "Flash",
    "アテンション": "Attention",
    "リベンジ": "Revenge",
    "シェイド": "Shade",
    "イルリヒト": "Irrlicht",
    "インドミタブル": "Indomitable",
    "フルゲージ": "Full Gauge",
    "チューン": "Tune",
    "ジャマー": "Jammer",
    "キュアヒール": "Cure Heal",
    "ダウナー": "Downer",
    "パフォーマンス": "Performance",
    "リヴァイタライズ": "Revitalize",
    "スマイト": "Smite",
    "ディープ": "Deep",
    "リフレッシュ": "Refresh",
    "スタブ": "Stub",
    "ブルーム": "Bloom",
    "ジャマ―": "Jammer",
    "フォース": "Force",
    "オーラ": "Aura",
    "ダークネス": "Darkness",
    "サヴァイヴ": "Survive",
    "ミュート": "Mute",
    "クウェル": "Cower",
    "シールマギア": "Seal Magia",
    "ワールウィンド": "Whirlwind",
    "アクセル": "Accele",
    "ブレイズン": "Blazen",
    "ストライク": "Strike",
    "デバフ": "Debuff",
    "バーン": "Burn",
    "アブソリュート": "Absolute",
    "アストラル": "Astral",
    "カウンター": "Counter",
    "アタック": "Attack",
    "プロヴォーク": "Provoke",
    "クラウド": "Cloud",
    "ソウル": "Soul",
    "ハームフル": "Harmful",
    "チャージ": "Charge",
    "ブレイブ": "Brave",
    "スタン": "Stun",
    "クリティカル": "Critical",
    "フォティチュード": "Fortitude",
    "バインド": "Bind",
    "パリィ": "Parry",
    "クレバー": "Clever",
    "エンドア": "Endor",
    "カバーリング": "Covering",
    "ペネトレイト": "Penetrate",
    "モラール": "Morale",
    "エイミング": "Aiming",
    "エストック": "Estock",
    "アージェント": "Argent",
    "シールド": "Shield",
    "テクニカル": "Technical",
    "チェイス": "Chase",
    "アデプト": "Adept",
    "マギア": "Magia",
    "ファスト": "Fast",
    "マナ": "Mana",
    "ブースト": "Boost",
    "ドッペル": "Doppel",
    "リジェネレイト": "Regeneration",
    "ブラスト": "Blast",
    "フォッグ": "Fog",
    "ガード": "Guard",
    "カース": "Curse",
    "メズマライズ": "Mesmerize",
    "ディトゥシー": "Ditsy",
    "レジスト": "Resist",
    "レストア": "Restore",
    "ミスト": "Mist",
    "ヘルス": "Health",
    "チャーム": "Charm",
    "アイズ": "Eyes",
    "エッジ": "Edge",
    "ポイズン": "Poison",
    "ヴェノム": "Venom",
    "インデュア": "Endure",
    "エピソード": "Episode",
    "ウェポン": "Weapon",
    "リーサル": "Lethal",
    "フレイム": "Flame",
    "アクア": "Aqua",
    "サマー": "Summer",
    "メモリーズ": "Memories",
    "グリッター": "Glitter",
    "ライト": "Light",
    "クライシス": "Crisis",
    "カバー": "Cover",
    "ダーク": "Dark",
    "コンボプラス": "Combo Plus",
    "ティンバー": "Timber",
    "ゴーストマーチ": "Ghost March",
    "アシッド": "Acid",
    "ノーブル": "Noble",
    "ヴァリアブル": "Variable",
    "ホーリー": "Holy",
    "デュオ": "Duo",
    "ダウン": "Down",
    "ブレイク": "Break",
    "ディリジェンス": "Diligence",
    "アピール": "Appeal",
    "スマッシュ": "Smash",
    "アベンジ": "Avenge",
    "コンボ": "Combo",
    "エキスパート": "Expert",
    "ヒーリング": "Healing",
    "ステップ": "Step",
    "アンカー": "Anchor",
    "デビル": "Devil",
    "テンプテーション": "Temptation",
    "チェイサー": "Chaser",
    "カタストロフ": "Catastrophe",
    "ヴィクトリーロード": "Victory Road",
    "デストロイ": "Destroy",
    "アウトバースト": "Outburst",
    "アーマメント": "Armament",
    "ウォール": "Wall",
    "コンバージョン": "Conversion",
    "ベール": "Veil",
    "エンハンス": "Enhance",
    "リフレクション": "Reflection",
    "ファランクス": "Phalanx",
    "イグノア": "Ignore",
    "アドレナリンラッシュ": "Adrenaline Rush"
}

# Subset of good effects that might be chance to happen
CHANCE_SKILLS = {"PURSUE", "AVOID", "PROVOKE", "CRITICAL", "PROTECT", "DEFENSE_IGNORED", "SKILL_QUICK", "COUNTER"}

with open("existing_translations.json", "r", encoding="utf-8") as f:
    existing_translations = [(w[0], w[1]) for w in json.load(f).items()]
    existing_translations.sort(reverse=True, key=lambda w: len(w[0]))


def translate_jap_to_eng(string):
    for jap_text, eng_text in existing_translations:
        string = string.replace(jap_text, eng_text)
    for jap_text, eng_text in jp_to_en.items():
        string = string.replace(jap_text, eng_text)
    return string


target_tl = {
    "TARGET": "Target",
    "SELF": "Self",
    "ALL": "All",
    "ONE": "One Ally",
    "DYING": "Self",
    "CONNECT": "Self"
}


def translate(shortDescription: str, arts: list[dict], include_roman: bool, include_100_percent: bool):
    romans = [roman_to_full[i] for i in re.findall(r"""\[(.*?)]""", shortDescription)]
    effects = {}
    icon = ""
    idx = 0

    art_ids = []
    first_effect = True
    for art in arts:
        may_use_roman = True
        art_id = art["artId"]
        art_ids.append(art_id)

        if "effectCode" in art:
            effect_code = art["effectCode"]
        else:
            effect_code = None
        verb_code = art["verbCode"]

        try:
            sub = master[verb_code]
        except KeyError as e:
            print("UNKNOWN verbCode   =", verb_code, "in master", art)
            raise e
        try:
            try:
                text, uses_roman, no_states_target = sub[effect_code]
            except KeyError:
                text, uses_roman, no_states_target = sub[art["targetId"]]
            if not icon:
                icon = text
                if verb_code in ("BUFF_HPMAX", "BUFF_PARTY_DIE", "BUFF_DIE"):
                    icon = str(icon.split()[0]) + " Up"
                elif effect_code in ("AUTO_HEAL",) and "genericValue" in art and art["genericValue"] == "MP":
                    icon = icon.replace("HP", "MP")
            if effect_code == "DUMMY":
                continue
            try:
                percentage_growth = round(art["growPoint"] / 10, 1)
            except KeyError:
                percentage_growth = 0
            if percentage_growth % 1 == 0:
                percentage_growth = int(percentage_growth)
            percentage_growth = f"{percentage_growth}%"

            val = 0
            if "effectValue" in art:
                if verb_code in ("TURN_ENEMY", "TURN_ALLY"):
                    art["enableTurn"] = art["effectValue"]  # Extend buffs/debuffs lists its duration under effectValue
                    del art["effectValue"]
                else:
                    val = round(art["effectValue"] / 10, 1)
            pro = 0
            if "probability" in art:
                pro = round(art["probability"] / 10, 1)

            if val % 1 == 0:
                val = int(val)
            if pro % 1 == 0:
                pro = int(pro)

            try:
                target_id = art["targetId"]
                target = target_tl[target_id]
                # Differentiates between effects that target all allies or all enemies by whether they are beneficial
                if target == 'All':
                    if verb_code in ("CONDITION_GOOD", "BUFF", "IGNORE", "LIMITED_ENEMY_TYPE", "TURN_ALLY") or (
                            verb_code == 'REVOKE' and effect_code in ("BAD", "DEBUFF")) or (
                            verb_code == "HEAL" and effect_code in ("HP", "MP")):
                        target = "Allies"
                    else:
                        target = "All Enemies"
                elif effect_code == "PROTECT":
                    target = "Self"
                    no_states_target = False
                    if target_id == "DYING":
                        text = text.replace("Guardian", "Guardian on Allies with Critical Health")
                elif target_id == "ONE":
                    if verb_code in ("HEAL",):
                        target = "Lowest HP Ally"
                    elif verb_code in ("RESURRECT",):
                        target = "Random Ally"

            except KeyError:
                target_id = "X"
                target = ""

            if "Down" in text and (text + target_id[0]) in effects:
                text = text.replace("Down", "Down Further")
            if "limitedValue" in art:
                limited_value = art["limitedValue"]
                if limited_value != "0":
                    target_chars = [girls[int(c)] for c in limited_value.split(",")]
                    target_chars_string = ""
                    if len(target_chars) > 1:
                        target_chars_string = ", ".join(target_chars[:-1]) + " and "
                    target_chars_string += target_chars[-1]
                    text += " to " + target_chars_string
                    may_use_roman = False

            if not val and not pro:
                effect = ""
            else:
                if pro and (val >= 100 or val == 0):
                    if effect_code in ("BARRIER",):
                        effect = val
                    elif verb_code in ("DRAW",) or effect_code in ("GUTS",  "NO_COST_CHARGE"):
                        effect = ""
                    elif effect_code in ("C_COMBO_PLUS",):
                        effect = int(val/100)
                    else:
                        effect = pro
                elif verb_code in ("ENCHANT", "CONDITION_BAD", "IGNORE") or effect_code in ("COUNTER", "PURSUE"):
                    effect = pro
                else:
                    effect = val
                if verb_code == "IGNORE" or (verb_code == "CONDITION_GOOD" and (
                        effect_code in CHANCE_SKILLS or effect_code == "IMITATE_ATTRIBUTE")):
                    if pro < 100:
                        text = "Chance to " + text
                    else:
                        effect = ""
                        uses_roman = False
                elif (verb_code == "CONDITION_BAD" and effect_code in bad) or verb_code == "ENCHANT":
                    if icon == text:
                        icon = "Chance to " + text
                    text = "Chance to " + text
                    if pro >= 100:
                        uses_roman = False
            if include_100_percent and effect == "" and verb_code not in ("REVOKE",) and effect_code not in (
                    "IMITATE_ATTRIBUTE",  "NO_COST_CHARGE"):
                effect = "100"

            if effect != "":
                if may_use_roman and ((include_roman and uses_roman) or (not include_roman and uses_roman and first_effect)):
                    try:
                        effect = f"{romans[idx]} / {effect}%"
                        idx += 1
                    except IndexError:
                        if idx > 0:
                            effect = f"{romans[idx - 1]} / {effect}%"
                        else:
                            effect = f"{effect}%"
                elif effect_code == "C_COMBO_PLUS":
                    effect = f"+{effect}"
                else:
                    effect = f"{effect}%"

            if effect_code in ("MP", "MP_DAMAGE", "MP_PLUS_WEAKED", "MP_PLUS_BLAST", "MP_PLUS_DAMAGED"):
                if verb_code == "INITIAL":
                    effect = effect.replace("%", "% full")
                else:
                    effect = effect.replace("%", " MP")
                    if percentage_growth != "0%":
                        percentage_growth = percentage_growth.replace("%", " MP")
            elif effect_code in ("AUTO_HEAL",) and "genericValue" in art and art["genericValue"] == "MP":
                text = text.replace("HP", "MP")
                effect = effect.replace("%", " MP")
                percentage_growth = percentage_growth.replace("%", " MP")
            elif verb_code in ("RESURRECT",) or effect_code in ("SURVIVE",):
                effect = effect.replace("%", "% HP")
                if percentage_growth != "0%":
                    percentage_growth = percentage_growth.replace("%", "% HP")
            if text == "Damage Up" and "ダメージアップ状態" in shortDescription:
                text = "Damage Increase"
            elif effect_code in ("COUNTER",) and val > 100:
                text = "Strengthened Counter"
            elif effect_code in ("POISON",) and val >= 30:
                text = text.replace("Poison", "Strengthened Poison")
            elif effect_code in ("CURSE",) and val >= 30:
                text = text.replace("Curse", "Strengthened Curse")
            elif effect_code in ("BARRIER",):
                effect = effect.replace("%", "0 damage")
            elif verb_code in ("IGNORE",):
                nr = art_ids.count(art_id)
                if effect_code in ("DEBUFF",):
                    effect = f"{nr} Debuff{'s' if nr > 1 else ''}"
                elif effect_code in ("CONDITION_BAD",):
                    effect = f"{nr} Status Ailment{'s' if nr > 1 else ''}"
            elif effect_code == "REFLECT_DEBUFF":
                effect = f"{int(val*10)} Debuff{'s' if val > 0.1 else ''}"

            if verb_code == "ATTACK" and "effectCode" in art:
                if art["effectCode"] in ("ALIGNMENT",):
                    text = text.replace("Damage", "Attribute Strengthened Damage")
                elif art["effectCode"] in ("DAMAGE_UP_BADS",):
                    text = text.replace("Damage", "Strengthened Damage") + " Affected with Status Ailments"

            try:
                turns = art["enableTurn"]
                if turns == 0:
                    turns = "∞"
            except KeyError:
                turns = 0

            # Move 1 down so thing w multiple effects only have 1 (target / X turns)?
            if turns and target and not no_states_target:  # enchant dont need target
                target_wording = f"{target} / {turns} Turn{'s' if turns != 1 else ''}"
            elif turns:
                target_wording = f"{turns} Turn{'s' if turns != 1 else ''}"
            elif target and ((target != "Self" and not no_states_target) or verb_code in ("REVOKE",) or (
                    effect_code in ("HP", "MP") and verb_code == "HEAL")):
                target_wording = str(target)
            else:
                target_wording = ""

            key = text + target_id[0]
            # Enables multi-effects other than Attack Down Further and Defense Down Further
            if text not in ("Anti-Debuff", "Negate Status Ailments") and key in effects:
                if len(effects[key]) == 4:
                    effects[key][3] += 1
                else:
                    effects[key].append(2)
            else:
                # Should refactor this somehow to separate allied and enemy casts without using a target_id key
                effects[key] = [effect, target_wording, percentage_growth]
        except KeyError as e:
            print("UNKNOWN effectCode =", art["effectCode"], shortDescription, art)
            raise e
        except IndexError as e:
            print("Missing roman in", shortDescription, romans, art)
            raise e
        first_effect = False
    return effects, icon


def remove_repeated_target(effects: dict):
    """Remove target if it's repeated multiple times"""
    prev_turn_counter = "TEMPLATE"
    for key in reversed(list(effects.keys())):
        current_turn_counter = effects[key][1]
        if current_turn_counter == prev_turn_counter:
            effects[key][1] = ""
        prev_turn_counter = current_turn_counter
