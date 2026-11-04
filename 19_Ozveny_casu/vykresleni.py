"""Grafické pomůcky a nabídky. Herní pravidla zůstávají v main.py.

Tento soubor lze při prvním čtení přeskočit. Funkce pouze kreslí.
"""

import pygame


BILA = (232, 242, 238)
TLUMENA = (151, 178, 187)
ZLATA = (255, 193, 105)
TYRKYSOVA = (109, 240, 228)
CERVENA = (255, 125, 112)


def text(plocha, font, obsah, x, y, barva=BILA, stred=False):
    obrazek = font.render(obsah, True, barva)
    rect = obrazek.get_rect()
    if stred:
        rect.midtop = (x, y)
    else:
        rect.topleft = (x, y)
    plocha.blit(obrazek, rect)


def panel(plocha, rect):
    pygame.draw.rect(plocha, (13, 32, 43), rect, border_radius=14)
    pygame.draw.rect(plocha, (50, 79, 87), rect, width=1, border_radius=14)


def tlacitko(plocha, font, rect, napis):
    barva = (255, 213, 149) if rect.collidepoint(pygame.mouse.get_pos()) else ZLATA
    pygame.draw.rect(plocha, barva, rect, border_radius=9)
    text(plocha, font, napis, rect.centerx, rect.y + 16, (18, 34, 40), True)


def vytvor_zari():
    zari = pygame.Surface((100, 100), pygame.SRCALPHA)
    for polomer in range(48, 0, -3):
        pygame.draw.circle(zari, (80, 235, 218, 48 - polomer), (50, 50), polomer)
    return zari


def kresli_menu(plocha, stav_hry, cislo_urovne, pocet_urovni, myslenka, fonty, tlacitka):
    """Stejné místo a tlačítka používají menu, pauza i výsledek."""
    male, normalni, velke, titulek = fonty
    hlavni_tlacitko, druhe_tlacitko = tlacitka
    ztmaveni = pygame.Surface(plocha.get_size(), pygame.SRCALPHA)
    ztmaveni.fill((3, 11, 18, 145))
    plocha.blit(ztmaveni, (0, 0))
    panel(plocha, pygame.Rect(160, 176, 620, 506))
    text(plocha, male, "ČASOVÝ EXPERIMENT / 19", 196, 205, TYRKYSOVA)
    if stav_hry == "menu":
        text(plocha, titulek, "OZVĚNY ČASU", 192, 246)
        radky = ["Nech svou minulost, aby ti pomohla.",
                 "1. Nahraj až 8 sekund cesty na desku A.",
                 "2. Ozvěna cestu zopakuje a zůstane na konci.",
                 "3. Dojdi na B. Obě desky odemknou východ."]
        napis = "VSTOUPIT DO LABORATOŘE"
    elif stav_hry == "pauza":
        text(plocha, titulek, "ČAS STOJÍ", 192, 246)
        radky = ["Hráč i jeho ozvěna čekají.", "Záznam ani přehrávání při pauze neběží.",
                 "MEZERNÍK řídí záznam, R vymaže pokus.", "Pokračuj klávesou ENTER nebo ESC."]
        napis = "POKRAČOVAT"
    else:
        nadpis = "ČAS JE TVŮJ" if stav_hry == "vyhra" else "CESTA OTEVŘENA"
        text(plocha, velke, nadpis, 196, 264, ZLATA)
        radky = [f"Dokončeno místností: {cislo_urovne + 1} / {pocet_urovni}",
                 myslenka,
                 "Jeden seznam poloh. Dvě verze stejné postavy.",
                 "Tvá minulá cesta pomohla té současné."]
        napis = "ZKUSIT ZNOVU" if stav_hry == "vyhra" else "DALŠÍ MÍSTNOST"
    for i, radek in enumerate(radky):
        text(plocha, male, radek, 196, 350 + i * 34, BILA if i == 0 else TLUMENA)
    tlacitko(plocha, normalni, hlavni_tlacitko, napis)
    tlacitko(plocha, normalni, druhe_tlacitko, "ZAVŘÍT" if stav_hry == "menu" else "HLAVNÍ MENU")
    text(plocha, male, "ENTER  potvrdit", 565, 550, TLUMENA)
