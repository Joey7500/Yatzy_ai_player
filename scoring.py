"""
Bodovani kategorii podle Yatzy
"""
from constants import Category

#vrati cestnost kostek v listu counts 4,4,5,5,5[0[0x] 1[0x] 2[0x] 3[0x] 4[2x] 5[3x] 6[0]]
def count_faces(dice: tuple[int, int, int, int, int]) -> list[int]:
    counts = [0] * 7  # index 0 nepouzivam, 1-6 pro hodnoty kostek
    for d in dice:
        counts[d] += 1
    return counts
    
# vypocita body pro kategorii v danem hodu, kdyz nejde kategorie vrati 0, vystup int cislo kategorie
def score_category(dice: tuple[int, int, int, int, int], cat: Category) -> int:
    counts = count_faces(dice)
    dice_sum = sum(dice)
    
    # upper section proste pocty cisel    
    if cat == Category.ONES:
        return counts[1] * 1
    elif cat == Category.TWOS:
        return counts[2] * 2
    elif cat == Category.THREES:
        return counts[3] * 3
    elif cat == Category.FOURS:
        return counts[4] * 4
    elif cat == Category.FIVES:
        return counts[5] * 5
    elif cat == Category.SIXES:
        return counts[6] * 6
    
    # dolni sekce
    elif cat == Category.THREE_KIND:
        # 3+ stejne soucet vsech kostek
        for value in range(1, 7):
            if counts[value] >= 3:
                return dice_sum
        return 0 #musim to osetrit protoze by mohlo to byt zvoleno ale nesplnit podminku
    
    elif cat == Category.FOUR_KIND:
        # 4+ stejne soucet vsech kostek
        for value in range(1, 7):
            if counts[value] >= 4:
                return dice_sum
        return 0 
    
    elif cat == Category.FULL_HOUSE:
        # 3 + 2 stejne = 25 bodu
        if 3 in counts and 2 in counts:
            return 25
        return 0

    elif cat == Category.SMALL_STRAIGHT:
        # Sekvence 4 po sobe 30 bodu
        sorted_unique = sorted(set(dice)) #set drzi jen unikatni hodnoty a seradime je
        for i in range(len(sorted_unique) - 3): 
            if sorted_unique[i:i+4] == list(range(sorted_unique[i], sorted_unique[i]+4)):
                return 30
        return 0
    
    elif cat == Category.LARGE_STRAIGHT:
        # Sekvence 5 po sobe = 40 bodu
        sorted_dice = tuple(sorted(dice))
        if sorted_dice == (1, 2, 3, 4, 5) or sorted_dice == (2, 3, 4, 5, 6):
            return 40
        return 0
    
    elif cat == Category.YAHTZEE:
        # 5 stejných = yatzy 50 bodu gratuluji
        if 5 in counts:
            return 50
        return 0
    
    elif cat == Category.CHANCE:
        # cokoliv soucet vsech savuje hry casto
        return dice_sum
    
    return 0 # fallback na 0 kdyby cat vratil neco jineho ale to se nestane xdd 
