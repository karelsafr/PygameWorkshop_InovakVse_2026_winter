"""Tři místnosti popsané obyčejnými řetězci.

# = zeď, . = podlaha, S = start, A a B = desky, D = dveře, E = východ.
Každá místnost má 16 sloupců a 9 řádků. Změnou znaků měníme hru.
"""

UROVNE = [
    {
        "nazev": "První ozvěna",
        "myslenka": "Ozvěna zopakuje tvou cestu a zůstane na jejím konci.",
        "napoveda": "Nahraj cestu na desku A. Ukonči záznam a dojdi na B.",
        "mapa": [
            "################",
            "#...........####",
            "#..A........####",
            "#...........#..#",
            "#.S.........D.E#",
            "#...........#..#",
            "#........B..####",
            "#...........####",
            "################",
        ],
    },
    {
        "nazev": "Za zdí",
        "myslenka": "Stejná pravidla fungují i v jiné místnosti.",
        "napoveda": "Nech ozvěnu na A. Zeď obejdi spodem a dojdi na B.",
        "mapa": [
            "################",
            "#.....#.....####",
            "#.S...#..B..####",
            "#.....#.....#..#",
            "#.....#.....D.E#",
            "#..A..#.....#..#",
            "#...........####",
            "#...........####",
            "################",
        ],
    },
    {
        "nazev": "Dlouhá vzpomínka",
        "myslenka": "Krátký záznam může později vykonat dlouhou cestu za tebe.",
        "napoveda": "Na A jdi horní chodbou a vpravo dolů. Pak čekej na B.",
        "mapa": [
            "################",
            "#...........####",
            "#....#......####",
            "#....#......#..#",
            "#....######.D.E#",
            "#....#......#..#",
            "#.SB.#...A..####",
            "#....#......####",
            "################",
        ],
    },
]
