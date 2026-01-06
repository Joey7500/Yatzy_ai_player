# 🎲 Yatzy AI Player (Expectimax)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
![Algorithm](https://img.shields.io/badge/Algorithm-Expectimax-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

> **Pokročilá implementace hry Yahtzee (Kostky) v Pythonu s využitím rozhodovacího stromu Expectimax a heuristických funkcí.**

Tento projekt implementuje kompletní pravidla hry Yahtzee a obsahuje **inteligentního AI agenta**, který dosahuje nadlidských výsledků (průměrně **~224 bodů** na hru) díky pravděpodobnostnímu vyhledávání a optimalizovaným heuristikám.

---

## ✨ Klíčové vlastnosti

- 🧠 **Smart AI (Expectimax)**:
  - Používá **rozhodovací strom** s uzly náhody (Chance nodes) a volby (Max nodes).
  - Počítá **očekávanou hodnotu (Expected Value)** každého hodu.
  - Dynamicky se rozhoduje, které kostky držet a které přehodit.
  
- ⚡ **Vysoký výkon**:
  - Využívá `@lru_cache` pro **memoizaci** stavů (cachování výpočtů).
  - Předpočítané kombinace hodů pro bleskurychlou expanzi stromu.
  - Bitové masky pro efektivní reprezentaci držených kostek.

- 🎮 **Herní módy**:
  - **Manuální hra**: Hrajte klasicky v terminálu.
  - **AI Advisor**: Hrajte sami, ale nechte si poradit od AI (zobrazuje "best move").
  - **AI Autoplay**: Sledujte AI, jak hraje celou hru za vás.
  - **Benchmark**: Rychlá simulace stovek her pro ověření statistické úspěšnosti.

- 🎨 **CLI Vizualizace**:
  - Krásné ASCII vykreslování kostek přímo v terminálu.
  - Přehledná skórovací tabulka (Scorecard).

---

## 🛠️ Instalace a Spuštění

Projekt nevyžaduje žádné externí knihovny (pouze standardní Python knihovny jako `random`, `functools`, `itertools`).

### 1. Klonování repozitáře
```bash
git clone https://github.com/your-username/yatzy-expectimax.git
cd yatzy-expectimax
