import re

roman_to_full = {
    "Ⅰ": "I",
    "Ⅱ" : "II",
    "Ⅲ": "III",
    "Ⅳ": "IV",
    "Ⅴ": "V",
    "Ⅵ": "VI",
    "Ⅶ": "VII",
    "Ⅷ": "VIII",
    "Ⅸ": "IX",
    "Ⅹ": "X",
    "XI": "XI",    
    "XII": "XII",    
    "XIII": "XIII",
    "ⅩⅢ": "XIII",
    "XIV": "XIV",    
    "XV": "XV",   
    "XⅤ": "XV",
    "XVI": "XVI",    
    "XVII": "XVII",
    "XVIII": "XVIII",
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

# Format is (description, uses_roman, includes_turns, no_state_target)

good = {
    "AUTO_HEAL": ("Regenerate HP", True, False),
    "PURSUE": ("Chance to Chase", True, False),
    "AVOID": ("Chance to Evade", True, False),
    "DAMAGE_DOWN": ("Damage Cut", True, False),
    "PROVOKE": ("Chance to Provoke", True, False),
    "GUTS": ("Endure", False, False),
    "MP_PLUS_WEAKED": ("MP Up When Attacked By Weak Element", True, False),
    "DAMAGE_DOWN_BLAST": ("Blast Damage Cut", True, False),
    "CRITICAL": ("Chance to Critical Hit", True, False),
    "PROTECT": ("Chance to Guardian", True, True),
    "DEFENSE_IGNORED": ("Chance to Defense Pierce", True, False),
    "SKILL_QUICK": ("Chance to Skill Quicken", True, False),
    "COUNTER": ("Chance to Counter", True, False),
    "DAMAGE_DOWN_ACCEL": ("Accele Damage Cut", True, False),
    "DAMAGE_DOWN_NODISK": ("Magia Damage Cut", True, False),
    "DAMAGE_DOWN_FIRE":("Flame Attribute Damage Cut", True, False),
    "DAMAGE_DOWN_TIMBER":("Forest Attribute Damage Cut", True, False),
    "DAMAGE_DOWN_DARK":("Dark Attribute Damage Cut", True, False),
    "DAMAGE_DOWN_LIGHT":("Light Attribute Damage Cut", True, False),
    "DAMAGE_DOWN_WATER":("Aqua Attribute Damage Cut", True, False),
    "DAMAGE_DOWN_VOID":("Void Attribute Damage Cut", True, False),
    "C_COMBO_PLUS": ("Charge Combo Charge Count Up (+1 / cannot be repeated)" , False, False),
    "MP_PLUS_DAMAGED": ("MP Up When Damaged", True, False),
    "DAMAGE_UP_BAD": ("Damage Up Versus Enemies Affected With Status Ailments", True, False),
    "SURVIVE": ("Survive", True, False),
    "MP_PLUS_BLAST" : ("Blast MP Gain Up", True, False),
    "DAMAGE_UP": ("Damage Up", True, False),
    "ATTACK_UP": ("Attack Up", True, False),  
    "IMITATE_ATTRIBUTE": ("Imitate Attribute", True, False),  
}

bad = {
    "CHARM": ("Chance to Charm", True, False),
    "POISON": ("Chance to Poison", True, False),
    "FOG": ("Chance to Fog", True, False),
    "CURSE": ("Chance to Curse", True, False),
    "BURN": ("Chance to Burn", True, False),
    "STUN": ("Chance to Stun", True, False),
    "BLINDNESS": ("Chance to Dazzle", True, False),
    "DARKNESS": ("Chance to Darkness", True, False),
    "BAN_SKILL": ("Chance to Skill Seal", True, False),    
    "BAN_MAGIA": ("Chance to Magia Seal", True, False),
    "RESTRAINT": ("Chance to Bind", True, False),
}

enchant = {
    "CHARM": ("Chance to Charm on Attack", True, True),
    "STUN": ("Chance to Stun on Attack", True, True),
    "POISON": ("Chance to Poison on Attack", True, True),
    "FOG": ("Chance to Fog on Attack", True, True),
    "BLINDNESS": ("Chance to Dazzle on Attack", True, True),
    "CURSE": ("Chance to Curse on Attack", True, True),        
    "BURN": ("Chance to Burn on Attack", True, True),    
    "DARKNESS": ("Chance to Darkness on Attack", True, True),
    "RESTRAINT": ("Chance to Bind on Attack", True, True),
    "BAN_SKILL": ("Chance to Skill Seal on Attack", True, True),    
    "BAN_MAGIA": ("Chance to Magia Seal on Attack", True, True),
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
    "DAMAGE": ("Damage Up", True, False),
}

ignore = {
    "BAN_SKILL": ("Chance to Anti-Skill Seal", True, False),
    "BAN_MAGIA": ("Chance to Anti-Magia Seal", True, False),
    "AVOID": ("Chance to Anti-Evade", True, False),
    "DEBUFF": ("Chance to Anti-Debuff", False, False),
    "COUNTER": ("Chance to Anti-Counter", True, False),
    "DAMAGE_DOWN": ("Ignore Damage Cut", True, False),
    "POISON": ("Chance to Anti-Poison", True, False),
    "CURSE": ("Chance to Anti-Curse", True, False),        
    "CHARM": ("Chance to Anti-Charm", True, False),    
    "BURN": ("Chance to Anti-Burn", True, False),
    "RESTRAINT": ("Chance to Anti-Bind", True, False),
    "PROVOKE": ("Chance to Anti-Provoke", True, False),
    "STUN": ("Chance to Anti-Stun", True, False),
    "FOG": ("Chance to Anti-Fog", True, False),
    "BLINDNESS": ("Chance to Anti-Dazzle", True, False),
    "DARKNESS": ("Chance to Anti-Darkness", True, False),
    "CRITICAL": ("Chance to Anti-Critical Hit", True, False),
}

revoke = {
    "BAD": ("Remove Status Ailments", False, False),
    "GOOD": ("Remove Buffs", False, False),
    "BUFF": ("Remove Buffs", False, False),
    "DEBUFF": ("Remove Debuffs", False, False),
}



buff_party_die = {
    "ATTACK" : ("Attack Up When Ally Dies", True, False),
    "DEFENSE" : ("Defense Up When Ally Dies", True, False),
}

buff_dying = {
    "ATTACK": ("Attack Up When At Critical Health", True, False),
    "DEFENSE" : ("Defense Up When At Critical Health", True, False),
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
    "WEAK_FIRE":("Flame Defense Down", True, False),
    "WEAK_TIMBER":("Forest Defense Down", True, False),
    "WEAK_DARK":("Dark Defense Down", True, False),
    "WEAK_LIGHT":("Light Defense Down", True, False),
    "WEAK_WATER":("Aqua Defense Down", True, False),
    "WEAK_VOID":("Void Defense Down", True, False),
    "MP_GAIN": ("MP Gain Down", True, False),
    "RESIST": ("Status Ailment Resistance Down", True, False),
    "MAGIA": ("Magia Damage Down", True, False),
    "ACCEL": ("Accele MP Gain Down", True, False),
    "BLAST": ("Blast Damage Down", True, False),
}

buff_hpmax = {
    "ATTACK": ("Attack Up While At Max Health", True, False),
    "DEFENSE" : ("Defense Up While At Max Health", True, False),
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
    "ONE": ("Revive one Ally", False, True),
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

master = {  # verbCode
    "CONDITION_GOOD" : good,
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
}

# Hard coded first before ・, general tls after
jp_to_en = {
    "受け継ぎし加護": "Inherited Protection",
    "ヘルスリカバリー": "Health Recovery",
    "MPブースト": "MP Boost",
    "フルスウィングアップ": "Full Swing Up",
    "イグノアデバフ": "Ignore Debuffs",
    "グリッターライズ": "Glitterise",
    "フルスウィング": "Full Swing Up",
    "クライシスブルーム": "Crisis Bloom",
    "スキルクイック": "Skill Quicken",
    "フルバースト": "Full Burst",
    "ピースフルカーム": "Peaceful Calm",
    "アタックライズ": "Attack Rise",    
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
    "アンチ・": "Anti-",
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
    "シールマギア": "Magia Seal",
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
    "アージェント": "Urgent",
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
}

target_tl = {
    "TARGET": "One",
    "SELF": "Self",
    "ALL": "All",
    "ONE": "One",
}

special = {
    "敵全体にダメージ & ２パターンの効果がランダムで発動": ({
        "Random Damage Effect & Random Pattern<br/>'''Pattern 1:''' Damage All Enemies [880%] & Defense Up (Allies / 3 Turns / 73.8%) & Damage Cut (Allies / 3 Turns / 50%) & HP Restore (Allies / 28%) <br/>'''Pattern 2:''' Damage All Enemies [902%] & Chance to Burn (All Enemies / 3 Turns / 50%) & Chance to Darkness (All Enemies / 1 Turn / 47.5%) & Chance to Bind (All Enemies / 1 Turn / 50%)": ("", "", ""),
        }, ""),
    }

def translate(shortDescription, arts):
    if shortDescription in special:
        return special[shortDescription]


    romans = [roman_to_full[i] for i in re.findall(r"""\[(.*?)]""", shortDescription)]
    effects = {}
    icon = ""
    idx = 0
    for art in arts:
        try:
            sub = master[art["verbCode"]]
        except KeyError as e:
            print("UNKNOWN verbCode   =", art["verbCode"], "in master", art)
            raise e
        try:
            try:
                text, uses_roman, no_states_target = sub[art["effectCode"]]
            except KeyError:
                text, uses_roman, no_states_target = sub[art["targetId"]]
            st = text
            if st == "Damage Up" and "状態" in shortDescription:
                st = "Damage Increase"
            if not icon:
                icon = text
            val = 0
            if "effectValue" in art:
                val = round(art["effectValue"] / 10, 1)
            pro = 0
            if "probability" in art:
                pro = round(art["probability"] / 10, 1)

            if val % 1 == 0:
                val = int(val)
            if pro % 1 == 0:
                pro = int(pro)

            if not val and not pro:
                effect = ""
            else:
                if pro and (val >= 100 or val == 0):
                    effect = pro
                elif art["verbCode"] == "ENCHANT" or art["verbCode"] == "CONDITION_BAD" or art["verbCode"] == "IGNORE":
                    effect = pro
                else:
                    effect = val

                if uses_roman:
                    try:
                        effect = f"{romans[idx]} / {effect}%"
                        idx += 1
                    except IndexError:
                        if idx > 0:
                            effect = f"{romans[idx-1]} / {effect}%"                            
                        else:
                            effect = f"{effect}%"
                    
                else:
                    effect = f"{effect}%"
            ef = effect
            try: 
                target = target_tl[art["targetId"]]
            except KeyError:
                target = ""
            try:
                turns = art["enableTurn"]
                if turns == 0:
                    turns = "∞"
            except KeyError:
                turns = 0

            # Move 1 down so thing w multiple efefcts only have 1 (target / X turns)?
            if turns and target and not no_states_target: # enchant dont need target  
                ta = "{} / {} Turn{}".format(target, turns, "s" if turns != 1 else "")
            elif turns:
                ta = "{} Turn{}".format(turns, "s" if turns != 1 else "")
            elif target and target != "Self" and not no_states_target:
                ta = "{}".format(target)
            else:
                ta = ""
            try:
                sc = round(art["growPoint"] / 10, 1)
            except KeyError:
                sc = 0
            if sc % 1 == 0:
                sc = int(sc)
            effects[st] = (ef, ta, f"{sc}%")
        except KeyError as e:
            print("UNKNOWN effectCode =", art["effectCode"], shortDescription, art)
            raise e
        except IndexError as e:
            print("Missing roman in", shortDescription, romans, art)
            raise e
    #¤print(shortDescription)
    #¤print(st)



    return effects, icon