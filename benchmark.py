"""
Benchmark AI hráče - spustí N her a vypíše statistiky.
"""
import random
import statistics
from typing import List, Optional
from game import play_game
from players import AIPlayer
from scorecard import ScoreCard

def run_benchmark(n_games: int, seed: Optional[int] = None, printing: bool = False) -> List[int]:
    """
    Spustí N her s AI hráčem a vrátí seznam skóre.
    """
    if seed is not None:
        random.seed(seed)
        
    scores = []
    
    print(f" Spouštím benchmark: {n_games} her...")
    print(f" Seed: {seed if seed is not None else 'random'}")
    print()
    
    for i in range(n_games):
        if (i + 1) % 100 == 0:
            print(f"   Dokončeno: {i + 1}/{n_games} her...")
        
        player = AIPlayer(printing=printing)
        final_scorecard = play_game(player, printing=printing, seed=None)
        scores.append(final_scorecard.total_score())
    
    return scores

def print_statistics(scores: List[int]):
    """Vypíše statistiky z benchmarku."""
    print("\n" + "=" * 60)
    print("           BENCHMARK VÝSLEDKY")
    print("=" * 60)
    print(f"Počet her:           {len(scores)}")
    print(f"Průměrné skóre:      {statistics.mean(scores):.2f}")
    print(f"Medián:              {statistics.median(scores):.2f}")
    print(f"Směrodatná odchylka: {statistics.stdev(scores):.2f}")
    print(f"Minimum:             {min(scores)}")
    print(f"Maximum:             {max(scores)}")
    print()
    print("Percentily:")
    try:
        quantiles = statistics.quantiles(scores, n=100) # Pro přesnější percentily
        print(f"  10%: {quantiles[9]:.1f}")  # 10. percentil
        print(f"  25%: {quantiles[24]:.1f}") # 25. percentil
        print(f"  50%: {statistics.median(scores):.0f}")
        print(f"  75%: {quantiles[74]:.1f}") # 75. percentil
        print(f"  90%: {quantiles[89]:.1f}") # 90. percentil
    except statistics.StatisticsError:
        # Fallback pro malý počet vzorků, kde quantiles může selhat
        print("  (Nedostatek dat pro detailní percentily)")
        
    print()
    print("Teoretický optimum: 254.59 (dle literatury)")
    print("=" * 60)
