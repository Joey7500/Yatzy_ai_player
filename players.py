"""
Hracske tridy, manualni lidsky, ai hrac a pak lidsky hrac s asistentem
"""
import random

from constants import N_DICE, SIDES, MAX_ROLLS_PER_TURN, Category, CATEGORY_NAMES
from scorecard import ScoreCard
from scoring import score_category
from expectimax_turn import recommend_action
from heuristics import choose_best_category

# cisla nejsou pekna, tak si definujeme jak maji vypadat
def dice_face(value: int) -> list[str]:
    faces = {
        1: [
            "┌─────────┐",
            "│         │",
            "│    ●    │",
            "│         │",
            "└─────────┘"
        ],
        2: [
            "┌─────────┐",
            "│ ●       │",
            "│         │",
            "│       ● │",
            "└─────────┘"
        ],
        3: [
            "┌─────────┐",
            "│ ●       │",
            "│    ●    │",
            "│       ● │",
            "└─────────┘"
        ],
        4: [
            "┌─────────┐",
            "│ ●     ● │",
            "│         │",
            "│ ●     ● │",
            "└─────────┘"
        ],
        5: [
            "┌─────────┐",
            "│ ●     ● │",
            "│    ●    │",
            "│ ●     ● │",
            "└─────────┘"
        ],
        6: [
            "┌─────────┐",
            "│ ●     ● │",
            "│ ●     ● │",
            "│ ●     ● │",
            "└─────────┘"
        ]
    }
    return faces.get(value, faces[1])

# vykreslime 5 kostek vedle sebe
def format_dice_visual(dice: tuple[int, ...]) -> str:
    dice_arts = [dice_face(d) for d in dice]
    
    # vytvor indexy
    indices = "  ".join(f"   [{i}]    " for i in range(len(dice)))
    
    # spoj vsech 5 kostek horizontalne
    lines = []
    for row in range(5):
        line = "  ".join(art[row] for art in dice_arts)
        lines.append(line)
    
    # pridej indexy nad kostky a vykresli
    return indices + "\n" + "\n".join(lines)


class TurnResult:
    """Vysledek jednoho tahu 3 hody a zapis do kategorie."""
    def __init__(self, final_dice, chosen_category, score):
        self.final_dice = final_dice
        self.chosen_category = chosen_category
        self.score = score

# napisu si tady metody spolecne pro vsechny hrace, take_turn bude klicovy rozdil pro kazdeho hrace
class Player():
    """ Trida hrace pro inheritenci"""
    def take_turn(self, scorecard: ScoreCard) -> TurnResult:
        pass
    
    #hodim kostkou random tuple
    def _roll_dice(self, n: int) -> tuple[int, ...]:
        return tuple(random.randint(1, SIDES) for _ in range(n))
    
    #reroll pokud si hrac zvolil ze nebude drzet vsechny
    def _reroll_dice(self, dice: tuple[int, ...], hold_mask: int) -> tuple[int, ...]:
        result = list(dice)
        for i in range(N_DICE):
            if not (hold_mask & (1 << i)):      #tady kouknu na hracovu masku a bitove udelam and s mymi kostkami
                result[i] = random.randint(1, SIDES) # kdyz je nedrzi, tak rereoll..
        return tuple(result)                         # koncim opet immutable tuplem coz je result drzenych a rerollovanych
    
    def _format_dice(self, dice: tuple[int, ...]) -> str:
        return "\n" + format_dice_visual(dice)


class AIPlayer(Player):
    """AI hrac pouziva expectimax strom"""
    
    def __init__(self, printing):   #Kvuli benchmarkovani a opakovanym spustenim si udelam vypisovaci boolean
        self.printing = printing
    
    def take_turn(self, scorecard: ScoreCard) -> TurnResult:
        """AI odehraje tah pomoci expectimax stromu."""
        
        
        # prvni roll
        dice = self._roll_dice(N_DICE)
        if self.printing:
            print(f"\n  První hod:{self._format_dice(dice)}")
            
        
        # Až 2 rerolly
        for reroll_num in range(1, MAX_ROLLS_PER_TURN):
            rerolls_left = MAX_ROLLS_PER_TURN - reroll_num
            
            rec = recommend_action(dice, rerolls_left, scorecard)
            
            if self.printing:
                held_idx = rec.held_indices()
                reroll_idx = rec.reroll_indices()
                print(f"  \"AI\" drží indexy: {held_idx}, přehazuje: {reroll_idx}")
                print(f"    (očekávaná hodnota: {rec.expected_value:.1f})")
                if rec.target_category:
                    print(f"     Cíl (může být i \"fallback\"): {CATEGORY_NAMES[rec.target_category]}")
            if rec.hold_mask == 31:
                break
            
            dice = self._reroll_dice(dice, rec.hold_mask)
            if self.printing:
                print(f"  Hod {reroll_num + 1}:{self._format_dice(dice)}")
        
        # Vyber kategorie z expectimax a heuristik
        best_cat, _ = choose_best_category(dice, scorecard)
        score = score_category(dice, best_cat)
        
        if self.printing:
            print(f"  \"AI\" zapisuje do {CATEGORY_NAMES[best_cat]}: {score} bodů")
        
        return TurnResult(dice, best_cat, score)
    

class HumanPlayer(Player):
    """Lidsky hrac"""
    
    def __init__(self, advisor: bool = False): # advisor jako boolean kvuli ciste lidskemu modu a modu s napovedou od "AI"
        self.advisor = advisor
    
    def take_turn(self, scorecard: ScoreCard) -> TurnResult:
        # Prvni hod
        dice = self._roll_dice(N_DICE)
        print(f"\n  První hod:{self._format_dice(dice)}")
        
        for reroll_num in range(1, MAX_ROLLS_PER_TURN):
            rerolls_left = MAX_ROLLS_PER_TURN - reroll_num
            
            # mame mod s advisorem nebo bez
            if self.advisor:
                rec = recommend_action(dice, rerolls_left, scorecard)
                print(f"\n\"AI\" doporučuje držet indexy: {rec.held_indices()}")
                if rec.target_category:
                    print(f"     Cíl (může být i \"fallback\"): {CATEGORY_NAMES[rec.target_category]}")

            print('-'*60)
            print(f"    Pro držení kostek zadej indexy kostek (0-4, oddělené mezerou):")
            print("    ENTER pro držení všech:")
            print("    'all' pro přehození všech:")
            
            inp = input("  Write > ").strip().lower() #mezery ani case nezalezi
            
            if inp == "":
                break  # drzim vse, konec
            
            if inp == "all":
                hold_mask = 0  # Přehazujeme všechny
            else:
                try:
                    held_indices = [int(x) for x in inp.split()] # ze stringu int seznam pomoci splitu
                    hold_mask = sum(1 << i for i in held_indices if 0 <= i < N_DICE) # suma "slepi bitove masky"
                except:
                    print("  Neplatný vstup, držím vše.")
                    break
                
                if hold_mask == 31:
                    break  # kdyz je input [0 1 2 3 4] -> bitove 11111 -> 31
            
            dice = self._reroll_dice(dice, hold_mask) # tady se uskutecni samotny reroll s maskou
            print(f"\n  Hod {reroll_num + 1}:{self._format_dice(dice)}")

        # zobraz finalni hod
        print(f"\n  Finální hod:{self._format_dice(dice)}")
        available = scorecard.available_categories()
        
        print("\n  Dostupné kategorie:")
        for i, cat in enumerate(available):
            pts = score_category(dice, cat)
            print(f"    {i}: {CATEGORY_NAMES[cat]:20s} = {pts:3d} bodů")
        
        if self.advisor:
            best_cat, best_val = choose_best_category(dice, scorecard)
            print(f"\n AI doporučuje: {CATEGORY_NAMES[best_cat]}")
        
        while True:
            try:
                choice = int(input("\n  Vyber kategorii (číslo): "))
                chosen_cat = available[choice]
                break
            except:
                print("  Neplatná volba, zkus znovu.")
        
        score = score_category(dice, chosen_cat)
        print(f"  Zapisuješ do {CATEGORY_NAMES[chosen_cat]}: {score} bodů")
        
        return TurnResult(dice, chosen_cat, score)
    
