"""

EXPECTIMAX STROM - JÁDRO AI HRÁČE

"""

from typing import Optional
from itertools import product
from functools import lru_cache #super vec pro memorizaci a zrychleni
from constants import N_DICE, SIDES, Category
from scorecard import ScoreCard
from heuristics import choose_best_category

# Predpocitame si outcomes dictionary pro optimalizaci rychlosti pres product, ktery je useful...
_OUTCOMES = {n: tuple(product(range(1, SIDES + 1), repeat=n))for n in range(1, N_DICE + 1)}

class Recommendation:
    def __init__(self,hold_mask: int,target_category:Optional[Category],expected_value:float):
        self.hold_mask = hold_mask                    # Bitmask: ktere kostky drzet 1 = drzet
        self.target_category = target_category          # cilova kategorie, nemusi byt zrejma, muze to byr i fallback
        self.expected_value = expected_value            # Ocekavana hodnota tahu
    
    def held_indices(self) -> list[int]:
        """vrati list indexu drzenych kostek"""
        return [i for i in range(N_DICE) if self.hold_mask & (1 << i)]
    
    def reroll_indices(self) -> list[int]:
        """vrati seznam indexu prehazovanych kostek"""
        return [i for i in range(N_DICE) if not (self.hold_mask & (1 << i))]


def recommend_action(dice: tuple[int, ...], rerolls_left: int, scorecard: ScoreCard) -> Recommendation:
    """
    Analyzuje aktualni stav a vrati doporuceni
    Prevadi logiku ze serazenych kostek (kvuli cache) na puvodni indexy.
    """
    # kvuli cache
    sorted_dice = tuple(sorted(dice))
    
    if rerolls_left == 0:
        best_cat, best_value = choose_best_category(sorted_dice, scorecard)
        return Recommendation(31, best_cat, best_value)
    
    # Nejlepsi maska pro serazene kostky, 
    # max pak zavlolla chance a vznikne struktura MAX -> CHANCE -> MAX2 -> CHANCE2
    best_mask_sorted, best_value = _max_node(sorted_dice, rerolls_left, scorecard)
    
    # Zjistíme hodnoty kostek, které chce AI držet
    values_to_hold = []
    for i in range(N_DICE):
        if best_mask_sorted & (1 << i):
            values_to_hold.append(sorted_dice[i])
    
    # Najdeme odpovidajici hodnoty 'dice'
    final_mask = 0
    used_indices = set()
    
    for val in values_to_hold:
        for i, d in enumerate(dice):
            if d == val and i not in used_indices:
                final_mask |= (1 << i)
                used_indices.add(i)
                break
    
    target = _guess_target_category(sorted_dice, best_mask_sorted, scorecard)
    
    return Recommendation(
        hold_mask=final_mask,
        target_category=target,
        expected_value=best_value
    )

@lru_cache(maxsize=300_000) # inicializujeme tu smart cachce vec co nude setrit pamet
def _max_node(dice: tuple[int, ...],rerolls_left: int,scorecard: ScoreCard) -> tuple[int, float]:
    """
    MAX UZEL - Hráč volí optimální akci
    OPTIMALIZACE:
    - Memoizace pomocí cache (stejné stavy = stejná rozhodnutí)
    - Cache klíč: (dice, rerolls_left, filled_mask, upper_sum)
    """
    assert rerolls_left > 0 #MAX uzel potřebuje rerolls_left > 0

    # Inicializace: první maska a jeji hodnota jako baseline
    best_mask = 0
    best_value = float('-inf')

    # iteruj pres vsech 32 hold mask
    for hold_mask in range(32):  # 2^5 = 32 možností
        
        # Urci co drzime a co prehazujeme
        held_dice = tuple(dice[i] for i in range(N_DICE) if hold_mask & (1 << i))
        n_reroll = N_DICE - len(held_dice) # pocet prehazovanych
        
        # Specialni pripad drzime vse, zadny reroll
        if n_reroll == 0:
            _, value = choose_best_category(dice, scorecard)
        else:
            #Normalni pripad, mame co prehazovat, chance uzel
            value = _chance_node(held_dice, n_reroll, rerolls_left - 1, scorecard) # tady ta -1 dulezita mega
            # tohle je vlastne ta rekurze, kde max vola chance
        
        # Aktualizuj best, pokud jsme nasli lepsi
        if value > best_value:
            best_value = value
            best_mask = hold_mask
    
    return best_mask, best_value

@lru_cache(maxsize=300_000)
def _chance_node( held_dice: tuple[int, ...], n_reroll: int, rerolls_left: int, scorecard: ScoreCard) -> float:
    """
    CHANCE UZEL - Náhoda určuje výsledek hodu
    """
    assert n_reroll > 0 #CHANCE uzel potřebuje n_reroll > 0
    
    total_value = 0.0
    n_outcomes = 0
    
    # Generuj vysledky rerollu
    for new_dice in _OUTCOMES[n_reroll]:
        
        # spoj drzene s prehozenymi
        combined = tuple(sorted(held_dice + new_dice))
        
        # kam dal ve stromu?
        if rerolls_left == 0:
            # Tim padem je to list a nasleduje evaluace pres heuristiky....
            _, value = choose_best_category(combined, scorecard)
        else:
            # stale mame rerolly, dalsi max uzel...
            _, value = _max_node(combined, rerolls_left, scorecard)
        
        total_value += value
        n_outcomes += 1
    
    # Ocekavana hodnota je prumer pres vsechny vysledky a to vraci...
    expected_value = total_value / n_outcomes
    
    return expected_value


def _guess_target_category(
    dice: tuple[int, ...],
    hold_mask: int,
    scorecard: ScoreCard
) -> Optional[Category]:
    """
    jen pokus o odhad kategorie pro uzivatele, muze byt none i uplne mimo, kvuli fallbacku...
    """
    held = tuple(dice[i] for i in range(N_DICE) if hold_mask & (1 << i))
    
    if not held:
        return None
    
    from collections import Counter
    counts = Counter(held)
    max_count = max(counts.values())
    
    # Heuristiky
    if max_count >= 4 and Category.YAHTZEE not in scorecard.available_categories():
        return None  # Už nemůžeme cílit na Yahtzee
    
    if max_count >= 4:
        return Category.YAHTZEE
    
    if max_count == 3:
        return Category.THREE_KIND
    
    # Zkusíme najít nejlepší kategorii pro současný hod jako hint
    try:
        cat, _ = choose_best_category(dice, scorecard)
        return cat
    except:
        return None

def clear_ai_cache():
    _max_node.cache_clear()
    _chance_node.cache_clear()
