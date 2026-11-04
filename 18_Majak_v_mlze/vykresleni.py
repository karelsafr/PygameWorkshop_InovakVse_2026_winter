"""Grafické pomůcky. Při prvním čtení hry můžeš tento soubor přeskočit.

Funkce pouze kreslí předaný stav; nerozhodují o pohybu, energii ani záchraně.
"""

import pygame

ZLATA = (244, 198, 110)
BILA = (239, 242, 235)
TLUMENA = (165, 187, 199)


def text(plocha, font, obsah, x, y, barva=BILA, stred=False):
    obrazek = font.render(obsah, True, barva)
    rect = obrazek.get_rect()
    if stred:
        rect.midtop = (x, y)
    else:
        rect.topleft = (x, y)
    plocha.blit(obrazek, rect)


def panel(plocha, rect, alpha=220):
    pozadi = pygame.Surface(rect.size, pygame.SRCALPHA)
    pygame.draw.rect(pozadi, (8, 21, 35, alpha), pozadi.get_rect(), border_radius=16)
    plocha.blit(pozadi, rect)


def tlacitko(plocha, font, rect, napis):
    barva = (255, 216, 139) if rect.collidepoint(pygame.mouse.get_pos()) else ZLATA
    pygame.draw.rect(plocha, barva, rect, border_radius=10)
    text(plocha, font, napis, rect.centerx, rect.y + 16, (24, 34, 41), True)


def vytvor_zari(polomer):
    """Jednou připravíme jemnou záři, kterou pak jen blitujeme."""
    obrazek = pygame.Surface((polomer * 2, polomer * 2))
    for r in range(polomer, 0, -4):
        sila = 1 - r / polomer
        barva = (int(25 * sila), int(15 * sila), int(4 * sila))
        pygame.draw.circle(obrazek, barva, (polomer, polomer), r)
    return obrazek


def kresli_noc(plocha, pozice_hrace, sviti, zare, bezpeci, dosah_svetla):
    """Průhledná tmavá vrstva má světlejší místa kolem obou světel."""
    noc = pygame.Surface(plocha.get_size(), pygame.SRCALPHA)
    noc.fill((3, 12, 27, 92))
    svetla = [(bezpeci, 115)]
    if sviti:
        svetla.append((pozice_hrace, dosah_svetla + 20))
    for stred, polomer in svetla:
        otvor = pygame.Surface((polomer * 2, polomer * 2), pygame.SRCALPHA)
        otvor.fill((255, 255, 255, 255))
        for r in range(polomer, 0, -5):
            alpha = int(92 * (r / polomer) ** 2)
            pygame.draw.circle(otvor, (3, 12, 27, alpha), (polomer, polomer), r)
        # V překryvu světel ponecháme menší krytí, tedy více světla.
        noc.blit(otvor, (stred[0] - polomer, stred[1] - polomer),
                 special_flags=pygame.BLEND_RGBA_MIN)
    plocha.blit(noc, (0, 0))
    if sviti:
        plocha.blit(zare, pozice_hrace - (dosah_svetla, dosah_svetla),
                    special_flags=pygame.BLEND_RGB_ADD)


def vytvor_mlhu():
    """Připravíme jeden průhledný obrázek, který se pak posouvá po pláži."""
    mlha = pygame.Surface((560, 150), pygame.SRCALPHA)
    for i in range(16):
        pygame.draw.ellipse(mlha, (165, 190, 210, i), (i * 10, i * 3, 560 - i * 20, 150 - i * 6))
    return mlha


def kresli_menu(plocha, stav_hry, pocet_zachranenych, sekundy, fonty, tlacitka):
    """Menu, pauza a výsledek používají stejné dva obdélníky tlačítek."""
    male, normalni, velke, titulek = fonty
    hlavni_tlacitko, druhe_tlacitko = tlacitka
    panel(plocha, pygame.Rect(44, 124, 550, 586), 240)
    text(plocha, male, "JEDNO SVĚTLO. OSM LIDÍ NA POBŘEŽÍ.", 76, 158, ZLATA)
    if stav_hry == "menu":
        text(plocha, titulek, "MAJÁK", 72, 204)
        text(plocha, titulek, "V MLZE", 72, 282)
        radky = ["Najdi trosečníky a doveď je do bezpečí.",
                 "Světlo lucerny je přiměje následovat tě.",
                 "Se Shiftem zpomal, ať skupině neutečeš.",
                 "U majáku doplníš energii. Máš tři minuty."]
        for i, radek in enumerate(radky):
            text(plocha, normalni, radek, 76, 402 + i * 32, TLUMENA)
        napis = "Vyrazit na pobřeží"
    else:
        nadpis = {"pauza": "CHVÍLE KLIDU", "vyhra": "VŠICHNI DOMA", "prohra": "NOC SKONČILA"}
        text(plocha, velke, nadpis[stav_hry], 76, 224, ZLATA)
        if stav_hry == "pauza":
            radky = ["Čas i energie lucerny jsou zastavené.",
                     "Enter nebo Escape pokračuje ve hře.",
                     "F1 ukáže stavy postav a dosah světla."]
        elif stav_hry == "vyhra":
            radky = ["Všech osm trosečníků je v bezpečí.",
                     f"Zbývající čas: {sekundy // 60}:{sekundy % 60:02}.",
                     "Maják dnes svítil pro všechny."]
        else:
            radky = [f"Do bezpečí jsi přivedl {pocet_zachranenych} z osmi lidí.",
                     "Zkus další hlídku. Se skupinou zpomal",
                     "a před dlouhou cestou dobij lucernu."]
        for i, radek in enumerate(radky):
            text(plocha, normalni, radek, 76, 330 + i * 38, TLUMENA)
        napis = "Pokračovat" if stav_hry == "pauza" else "Nová hlídka"
    tlacitko(plocha, normalni, hlavni_tlacitko, napis)
    text(plocha, male, "ENTER", 400, 585, TLUMENA)
    tlacitko(plocha, male, druhe_tlacitko, "Zavřít" if stav_hry == "menu" else "Hlavní menu")

