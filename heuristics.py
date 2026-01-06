"""
Heuristiky pro hodnocení tahů v expectimax stromu.
"""

from constants import Category, UPPER_CATEGORIES, UPPER_BONUS_THRESHOLD, UPPER_BONUS_VALUE
from scorecard import ScoreCard
from scoring import score_category



# Tuning konstanty tady se to menilo a dosel jsem na tyto hondoty...

# Bonus tlak (delta EV bonusu) – jak moc tlacim na bonus, jak moc je pro nas dulezity
BONUS_PRESSURE = 1.30

# Underfill penalizace v upper – aplikovat hlavne na vysoke face a spíš v early/mid
UPPER_UNDERFILL_PENALTY = 12.0
UPPER_UNDERFILL_MIN_TURNS = 6  # od kolika volnych kategorii to resit

# Jemná penalizace "lost potential"
# Penalizuje ztrátu maxima v upper, ale ne tak agresivně, aby to kazilo minimum.
UPPER_LOST_POTENTIAL = 0.30

# Extra penalizace: když v early zalepis vyssi kategorie jednou kostkou
UPPER_HIGHFACE_SINGLE_EXTRA = 6.0

# Nuly (proskrtneme kategorii)
ZERO_UPPER_BASE = 26.0
ZERO_RARE_BASE = 20.0
ZERO_LOWER_BASE = 10.0

# Chance: soft lock (ne “zamknout”, ale odrazovat)
CHANCE_LOCK_TURNS = 7         # kdyz je jeste hodne kategorii volnych, chance je vzacna volba
CHANCE_TARGET_EARLY = 23      # v early ber Chance jen kdyz je slusna takze cca 23 coz je dost
CHANCE_TARGET_MID = 21        # v mid je cil todhu nizsi
CHANCE_PENALTY_BASE = 10.0    # zaklad pro penalizaci chance
CHANCE_PENALTY_SLOPE = 1.4    # sklon funkce penalizacce

# slabe trojice a ctverice trestame v early game
LOW_THREE_KIND_PENALTY = 8.0
LOW_FOUR_KIND_PENALTY = 10.0


# Helpery
def _turns_left(scorecard: ScoreCard) -> int:
    # pocet volnych kategorii pred zapisem
    return len(scorecard.available_categories())

def _is_upper(cat: Category) -> bool:
    # je v horni kategorii?
    return cat in UPPER_CATEGORIES

def _upper_face_value(cat: Category) -> int:
    # prevede kategorii na cislo na kostce, Category.ONES = 0 -> face = 1... SIXES = 5 -> face = 6
    return int(cat) + 1

def _max_upper_points_for_cat(cat: Category) -> int:
    # Maximum pro danou upper kategorii je 5*face, tim ziskame potencial bodovy
    return 5 * _upper_face_value(cat)

def _remaining_upper(scorecard: ScoreCard) -> list[Category]:
    #jake kategorie zbyvaji?
    return [score for score in UPPER_CATEGORIES if not scorecard.is_filled(score)]

    #dulezita funkce, ktera odhadne float od 0 po 1 jako pravdepodobnost ze dostaneme bonus
def _bonus_probability(upper_sum: int, remaining_upper: list[Category]) -> float:
    """
    Hruby odhad pravdepodobnosti dosazeni bonusu 63.
    """
    need = UPPER_BONUS_THRESHOLD - upper_sum #kolik jeste potrebuju?
    if need <= 0:
        return 1.0

    max_remaining = sum(_max_upper_points_for_cat(c) for c in remaining_upper)
    if max_remaining <= 0:#kolik jeste muzu vytriskat ze zbyvajicich kategorii?
        return 0.0

    reserve = max_remaining - need # jakou mam rezervu
    p = reserve / max_remaining  # (-inf..1)
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0

    return p ** 1.7     #umocneno na 1.7 aby se chovalo konzervativne, takze umele trochu snizuje sanci...

def _bonus_ev(scorecard: ScoreCard) -> float:
    """ocekavana hodnota bonusu nam pomuze s rozhodovanim jestli jit po bonusu
    priradi bonusu cislo mezi 0 a 35 a na zaklade toho se budou pocitat optimalni tahy"""
    p = _bonus_probability(scorecard.upper_sum, _remaining_upper(scorecard)) 
    return p * UPPER_BONUS_VALUE

def _zero_upper_scale(face: int) -> float:
    """
  tady nacenujeme obeti, neboli zamerne proskrtnute kategorie
    """
    return 0.30 + 0.70 * ((face / 6.0) ** 1.4) # tenhle vzorec bere jako zaklad 0.3 a 
    # pricita k nemu jak moc ho boli obetovat vyssi a vyssi cisla, mocnina 1,4 dela mocninny prubeh, silnejsi nez linearni


# Hlavni heuristiky
def evaluate_write(dice: tuple[int, ...], scorecard: ScoreCard, cat: Category) -> float:
    """funkce vraci neco jako spokojenost AI, float toho jak se"""
    immediate = score_category(dice, cat)
    value = float(immediate)

    turns = _turns_left(scorecard)
    phase = turns / 13.0  # faze hry ma velky vliv na rozhodovani

    # Horni bonus se vyresi tak ze ke skutecne hodnote pricteme hodnotu za priblizeni k bonusu, 
    # je to nejdulezitejsi blok z hlediska strategie
    before = _bonus_ev(scorecard)

    if _is_upper(cat):
        after_upper_sum = scorecard.upper_sum + immediate
        after_remaining_upper = [score for score in _remaining_upper(scorecard) if score != cat]
        after_p = _bonus_probability(after_upper_sum, after_remaining_upper) #znovu zavolam tu funkci na to co by bylo kdybych to zapasal...
        after = after_p * UPPER_BONUS_VALUE #nova nadeje na bonus
    else:
        after = before

    value += BONUS_PRESSURE * (after - before) #nova hodnota pro srovnani s ostatnimi

    # 2) Chance: soft odrazovani v early/mid, chance je pro nas hodne dulezita kvuli paleni nevydarenych hodu
    if cat == Category.CHANCE:
        if turns >= CHANCE_LOCK_TURNS:
            target = CHANCE_TARGET_EARLY
        elif turns >= 4:
            target = CHANCE_TARGET_MID
        else:
            target = 0  # late game: klidně ji vem

        if target > 0 and immediate < target: #opovazil ses zapsat nejaky nizky hod? tady mas penalizaci...
            value -= (CHANCE_PENALTY_BASE + (target - immediate) * CHANCE_PENALTY_SLOPE) * phase
            # penalizace zavisi na rozdilu vuci targetu, pak na sklonu funkce (slope, aby velke preslapy trestal tvrde)
            #  a pak na fazi hry, na zacatku te to bude bolet 1.0

    # 3) Upper underfill + lost potential, proste brani aby si zapsala do 4,5,6 malo bodu
    if _is_upper(cat) and scorecard.upper_sum < UPPER_BONUS_THRESHOLD and turns >= UPPER_UNDERFILL_MIN_TURNS:
        face = _upper_face_value(cat)
        max_pts = 5 * face

        # (A) Underfill: hlavně pro face>=4, pro 2 a mene kostek
        if face >= 4 and immediate <= 2 * face:
            fill_ratio = immediate / max_pts if max_pts > 0 else 0.0
            value -= UPPER_UNDERFILL_PENALTY * (1.0 - fill_ratio) * phase
            # pomer zaplneni, penalizace a faze hry...

        # (B) Lost potential: Jemne penalizuj stratu vyssiho zisku, pro vyssi face vice face_weight
        lost = max_pts - immediate
        face_weight = (face / 6.0) ** 1.2  
        value -= UPPER_LOST_POTENTIAL * lost * face_weight * phase

        # (C) Extra: early nelep 5/6 jednou kostkou to by stalo strasne moc bodu
        if turns >= 7 and face >= 5 and immediate <= face:
            value -= UPPER_HIGHFACE_SINGLE_EXTRA * phase

    # 4) 3-kind / 4-kind penalizace nizkych vysledku kdyz jeste zbyva vic jak 6 hodu
    if cat == Category.THREE_KIND and turns >= 6:
        if 0 < immediate < 12:
            value -= LOW_THREE_KIND_PENALTY * phase

    if cat == Category.FOUR_KIND and turns >= 6:
        if 0 < immediate < 20:
            value -= LOW_FOUR_KIND_PENALTY * phase

    # 5) Nuly: skaluj upper podle face ONES/TWOS levnejsi a take neskrtej rare kategorie
    if immediate == 0:
            rare = {Category.LARGE_STRAIGHT, Category.SMALL_STRAIGHT, Category.FULL_HOUSE}

            if _is_upper(cat):
                face = _upper_face_value(cat)
                value -= ZERO_UPPER_BASE * _zero_upper_scale(face) * phase
                
            elif cat == Category.YAHTZEE:
                # Dynamicka hodnota Yahtzee podle faze hry
                if turns >= 8:
                    # Early game: Yahtzee je svate, neskrtej ho!
                    value -= (ZERO_RARE_BASE + 8.0) * phase
                elif turns >= 5:
                    # Mid game: Stale velmi cenne
                    value -= ZERO_RARE_BASE * phase
                else:
                    # Late game (posledni 4 tahy):
                    # Tady uz se k nemu chovej jako k "odpadu".
                    # Penalizace 2.0 je mensi nez ZERO_LOWER_BASE (10.0).
                    # To znamena:radeji skrtni Yahtzee nez treba Trojici nebo Jednicky.
                    value -= 2.0 * phase 

            elif cat in rare and turns >= 6:
                value -= ZERO_RARE_BASE * phase
            else:
                value -= ZERO_LOWER_BASE * phase

    # 6) Malý bonus za fixni velke kdyz padnou... na tady mas cukrik a rychle si to zapis
    if cat in (Category.LARGE_STRAIGHT, Category.SMALL_STRAIGHT, Category.FULL_HOUSE, Category.YAHTZEE):
        if immediate > 0:
            value += 2.0 * phase

    return value


def choose_best_category(dice: tuple[int, ...], scorecard: ScoreCard) -> tuple[Category, float]:
    """vyhodnotime pomoci evaluate_write nejlepsi ocekavanou hondotu a to zapiseme"""

    available = scorecard.available_categories()
    if not available:
        raise ValueError("Žádné dostupné kategorie!")

    best_cat = available[0] #vezmi prvni co mame a rekni ze je to mximum
    best_val = evaluate_write(dice, scorecard, best_cat) #spocitje jeho hondotu
    
    #vezmi druhou a dalsi... a porovnej
    for cat in available[1:]:
        v = evaluate_write(dice, scorecard, cat)
        if v > best_val:
            best_val = v
            best_cat = cat

    return best_cat, best_val   #vrat to nejlepsi co mas...
