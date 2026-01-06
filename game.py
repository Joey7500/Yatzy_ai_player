"""
Orchestrátor hry - řídí 13 kol Yahtzee.
"""
import random
from scorecard import ScoreCard
from players import Player
from expectimax_turn import clear_ai_cache
clear_ai_cache()

# printing je volitelny boolean hlavne kvuli benchmarku
def play_game(player: Player, printing: bool = True, seed: int = None) -> ScoreCard:
    """
    Odehraje kompletní hru Yahtzee (13 kol).
    
    Returns:
        Finální ScoreCard
    """
    if seed is not None:
        random.seed(seed)
    
    scorecard = ScoreCard()
    
    if printing:
        print("=" * 60)
        print("           YAHTZEE HRA - START")
        print("=" * 60)
    
    # 13 kol
    for round_num in range(1, 14):
        if printing:
            print(f"\n{'─' * 60}")
            print(f"KOLO {round_num}/13")
            print(f"{'─' * 60}")
        
        # Hráč odehraje tah
        result = player.take_turn(scorecard)
        
        # Aktualizuj scorecard
        scorecard = scorecard.with_score(result.chosen_category, result.score)
        
        if printing:
            print(f"\n{scorecard}")
    
    if printing:
        print("\n" + "=" * 60)
        print(f"           HRA SKONČILA")
        print(f"           FINÁLNÍ SKÓRE: {scorecard.total_score()}")
        print("=" * 60)
    
    return scorecard
