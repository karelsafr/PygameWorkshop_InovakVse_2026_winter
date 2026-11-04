Python v pohybu: Od prvních příkazů k vlastní hře
Autor workshopu: Ing. Karel Šafr, Ph.D.
4. listopadu 2026, 9:00-15:00, SB 321

OBSAH

Pygame2026_workshop_final.pptx / .pdf
    Prezentace k herní části workshopu, 103 snímků.

Izometrie_vysvetleni.pdf
    Jednostránkový přehled souřadnic a výpočtů izometrie.

Pohyb_hrace_vysvetleni.pdf
    Jednostránkový přehled vektorů, úhlů, rychlosti, zrychlení a času.

01_hello_world až 13_MINY, včetně 0x_SIM
    Postupné ukázky kódu s potřebnými obrázky a zvuky.
    Některé složky obsahují více variant skriptu.

18_Majak_v_mlze / 19_Ozveny_casu
    Dvě samostatné hry. Ovládání a vysvětlení jsou v jejich README.md.

AI_Cart_engine_PUBLIC
    Závodní engine pro trénování agentů. Začněte souborem README.md
    nebo STUDENT_GUIDE.md uvnitř projektu.

Python_opakovani
    Aktuální úvodní prezentace (99 snímků) a notebook quick_python.ipynb.
    Notebook otevřete v Jupyteru nebo editoru s podporou souborů .ipynb.
    Obsahuje také řešení příkladů.

PŘÍPRAVA PROSTŘEDÍ

Ukázky byly ověřeny s Pythonem 3.12 a pygame-ce 2.5.8.
Ve složce s tímto souborem vytvořte a aktivujte virtuální prostředí.

Windows:
    py -m venv .venv
    .venv\Scripts\activate
    python -m pip install -r requirements.txt

macOS / Linux:
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

Balíček se jmenuje pygame-ce, v kódu se používá import pygame.
NumPy a Matplotlib potřebuje simulace 0x_SIM a AI závodní engine.

SPUŠTĚNÍ

V aktivovaném prostředí přejděte do složky vybrané ukázky a spusťte
její soubor .py. Název se liší podle ukázky: například hello_world.py,
ball.py, car.py, Miny.py nebo main.py. Například:

    cd 18_Majak_v_mlze
    python main.py

AI engine spouštějte z jeho vlastní složky AI_Cart_engine_PUBLIC,
protože z ní načítá grafiku a mapy.

V AI enginu zůstává původní students/benchmark_agents.yaml se seznamem
dřívějších týmů. Jejich agenti a uložené modely nejsou v balíčku.
Před benchmarkem upravte tento seznam podle agentů a modelů, které
máte skutečně ve students/agents a students/saves. Podrobnosti uvádí
STUDENT_GUIDE.md. Základní spuštění a trénování tento seznam nepotřebují.

Podmínky použití přibalené grafiky najdete v doprovodných souborech
jednotlivých ukázek a grafických sad.
