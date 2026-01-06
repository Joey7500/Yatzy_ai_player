"""
CLI vstupní bod - menu pro výběr režimu hry.
"""
import sys
from game import play_game
from players import AIPlayer, HumanPlayer

def print_menu():
    """Vypíše hlavní menu."""
    print("=" * 60)
    print("           YAHTZEE AI - Expectimax Projekt")
    print("=" * 60)
    print("\nRežimy hry:")
    print("  1. \"AI\" hráč (autoplay)")
    print("  2. Lidský hráč")
    print("  3. Lidský hráč + AI asistent")
    print("  4. Benchmark (N her)")
    print("  5. Ukončit")
    print()

def main():
    while True:
        print_menu()
        choice = input("Vyber režim (1-5): ").strip()
        
        if choice == "1":
            
            # AI autoplay
            print("\n \"AI\" hráč hraje...")
            player = AIPlayer(printing=True)
            final = play_game(player, printing=True)
            print(f"\n \"AI\" skóre: {final.total_score()}")

        
        elif choice == "2":
            # Human
            print("\n Lidský hráč")
            player = HumanPlayer(advisor=False)
            final = play_game(player, printing=True)
            print(f"\n Tvoje skóre: {final.total_score()}")
        
        elif choice == "3":
            # Human + advisor
            print("\n Lidský hráč s \"AI\" asistentem")
            player = HumanPlayer(advisor=True)
            final = play_game(player, printing=True)
            print(f"\n Tvoje skóre: {final.total_score()}")
        
        elif choice == "4":
            # Benchmark
            try:
                n = int(input("Počet her (např. 1000): "))
            except:
                n = 1000
            
            from benchmark import run_benchmark, print_statistics
            scores = run_benchmark(n_games=n, seed=None, printing=False)
            print_statistics(scores)
        
        elif choice == "5":
            print("\n Konec")
            sys.exit(0)
        
        else:
            print("\n Invalid")
        
        input("\nStiskni Enter pro návrat do menu...")

if __name__ == "__main__":
    main()
