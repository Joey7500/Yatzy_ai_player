"""
ScoreCard - immutable reprezentace stavu vyplnenych kategorii
plus scitani bodu v upper a narok na upper bonus
"""
from dataclasses import dataclass, field
from typing import Optional #tenhle vec drzi None nebo int
from constants import (
    Category, ALL_CATEGORIES, UPPER_CATEGORIES, LOWER_CATEGORIES,  
    UPPER_BONUS_THRESHOLD, UPPER_BONUS_VALUE, CATEGORY_NAMES 
)


# tahle trida bude primarne pro drzeni dat, takze s to usnadnim a @dataclass mi vygeneruje  __init__ a
# krome toho mohu pouzit field s default_factory ktery dokaze kazde hre generovat dalsi novy seznam
@dataclass(frozen=True, slots = True) 
class ScoreCard:
    """
    Immutable reprezentace stavu scorecard.
    """
    filled_mask: int = 0                           # je to int ale pouzijeme ho jako bitmasku
    scores: tuple[Optional[int], ...] = field(
        default_factory=lambda: tuple([None] * len(ALL_CATEGORIES)) #https://dev.to/devasservice/python-trick-using-dataclasses-with-fielddefaultfactory-4159
    )
    upper_sum: int = 0                            # Součet bodů v horní části (pro bonus)

    
    def is_filled(self, cat: Category) -> bool: #kontrola vyplneni kategorie
        return bool(self.filled_mask & (1 << cat)) 
    """  tady je ta mechanika binarni masky... mam vyplnenou masku self.filled_mask a overim  
          zda je jednicka na pozici cat a tudis je kategorie vyplnena -> bool """
    
    def available_categories(self) -> list[Category]: # vraci nevyplnene kategorie
        return [cat for cat in ALL_CATEGORIES if not self.is_filled(cat)]
    
    def with_score(self, cat: Category, points: int) -> 'ScoreCard':
        """
        vraci aktualizovanou scorecard, tedy jelikoz je to immutable zkopiruje starou a prida nove veci tuple()
        """
        new_scores = list(self.scores) # tuple -> list kopie
        new_scores[cat] = points # zapis do cat indexu ziskane body
        new_mask = self.filled_mask | (1 << cat)
        
        new_upper = self.upper_sum
        if cat in UPPER_CATEGORIES:
            new_upper += points     # trackujeme upper skore kvuli bonusu +35
        
        return ScoreCard(
            filled_mask=new_mask,
            scores=tuple(new_scores),
            upper_sum=new_upper
        )
    
    def upper_bonus(self) -> int:
        """vrati bonus kdyz je to vetsi nez threshold 63"""
        return UPPER_BONUS_VALUE if self.upper_sum >= UPPER_BONUS_THRESHOLD else 0
    
    def total_score(self) -> int:
        """celkove skore kategorii plus pripadne bonus"""
        overall_score = sum(score for score in self.scores if score is not None)
        return overall_score + self.upper_bonus()
    
    def __str__(self) -> str: # prepisme defaultni print metodu a pri pouhem zavolani print()
        """Vypis Scorecard"""
        lines = ["-" * 40, "SCORECARD", "-" * 40]
        
        # Horni sekce prepopcitani plus vypsani
        lines.append("UPPER SECTION:")
        upper_total = 0
        for cat in UPPER_CATEGORIES:
            score = self.scores[cat]
            score_str = str(score) if score is not None else "-"
            lines.append(f"  {CATEGORY_NAMES[cat]:20s}: {score_str:>3s}")
            if score is not None:
                upper_total += score
        
        lines.append(f"  {'Upper Total':20s}: {upper_total:3d}")
        lines.append(f"  {'Bonus (63+)':20s}: {self.upper_bonus():3d}")
        lines.append(f"  {'Upper + Bonus':20s}: {upper_total + self.upper_bonus():3d}")
        
        # Dolní sekce prepocitani a vypsani
        lines.append("\nLOWER SECTION:")
        lower_total = 0
        for cat in LOWER_CATEGORIES:
            score = self.scores[cat]
            score_str = str(score) if score is not None else "-"
            lines.append(f"  {CATEGORY_NAMES[cat]:20s}: {score_str:>3s}")
            if score is not None:
                lower_total += score
        
        lines.append(f"  {'Lower Total':20s}: {lower_total:3d}")
        lines.append("=" * 40)
        lines.append(f"  {'TOTAL SCORE':20s}: {self.total_score():3d}")
        lines.append("=" * 40)
        
        return "\n".join(lines) #slep lines a oddel je entrama
