"""
Konstanty hry Yatzy.
"""
from enum import IntEnum # typ pro pojmenovana cisla, jsou to pojmenovani a zaroven int takze mohou slouzit i k indexaci/bit pozicovani


N_DICE = 5                    # 5 kostek ve hre
SIDES = 6                     # kostka ma 6 stran
MAX_ROLLS_PER_TURN = 3        # hod a dva prhozy

## Horni bonus
UPPER_BONUS_THRESHOLD = 63    # Pri 63 a vic muzes ziskas bonus
UPPER_BONUS_VALUE = 35        # ziskas 35 bodu

## 13 kategorii skorovani
class Category(IntEnum):
    # upper sekce
    ONES = 0
    TWOS = 1
    THREES = 2
    FOURS = 3
    FIVES = 4
    SIXES = 5
    
    # lower sekce
    THREE_KIND = 6        # 3 stejne  = soucet vsech
    FOUR_KIND = 7         # 4 stejné = soucet vsech
    FULL_HOUSE = 8        # 3 + 2 stejne = 25 bodu
    SMALL_STRAIGHT = 9    # 4 za sebou = 30 bodu
    LARGE_STRAIGHT = 10    # 5 za sebou = 40 bodu
    YAHTZEE = 11          # 5 stejnych  = 50 bodu
    CHANCE = 12            # cokoliv = soucet vsech / pojistka spatneho hodu


# pro prehlednost to zabalim do listu all upper a lower
# hlavne je to protoze upper sum ma bonus...

ALL_CATEGORIES = list(Category)

UPPER_CATEGORIES = [
    Category.ONES, Category.TWOS, Category.THREES,
    Category.FOURS, Category.FIVES, Category.SIXES,
]

LOWER_CATEGORIES = [
    Category.THREE_KIND, Category.FOUR_KIND, Category.FULL_HOUSE,
    Category.SMALL_STRAIGHT, Category.LARGE_STRAIGHT,
    Category.YAHTZEE, Category.CHANCE
]


#mapovani jmeno pro UI, aby to bylo citelne tak proste dict
CATEGORY_NAMES = {
    Category.ONES: "Ones",
    Category.TWOS: "Twos",
    Category.THREES: "Threes",
    Category.FOURS: "Fours",
    Category.FIVES: "Fives",
    Category.SIXES: "Sixes",
    Category.THREE_KIND: "Three of a Kind",
    Category.FOUR_KIND: "Four of a Kind",
    Category.FULL_HOUSE: "Full House",
    Category.SMALL_STRAIGHT: "Small Straight",
    Category.LARGE_STRAIGHT: "Large Straight",
    Category.YAHTZEE: "Yahtzee",
    Category.CHANCE: "Chance"
}
