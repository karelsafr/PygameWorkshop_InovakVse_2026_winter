"""Ozvěny času – záznam pohybu jako obyčejný seznam dat."""

from pathlib import Path
import pygame

from postavy import Hrac, Ozvena
from urovne import UROVNE
from vykresleni import (
    BILA, TLUMENA, ZLATA, TYRKYSOVA, CERVENA,
    text, panel, vytvor_zari, kresli_menu,
)


# 1. KONSTANTY – pravidla i rozměry jsou na jednom místě.
SIRKA, VYSKA = 1280, 800
FPS = 60
DLAZDICE = 64
MAPA_X, MAPA_Y = 128, 140
DELKA_ZAZNAMU = 8
DOBA_SEPNUTI = 0.6
SLOZKA = Path(__file__).parent


# 2. POMOCNÉ FUNKCE – načtení dat a malé kreslicí operace.
def nacti_snimky(jmeno):
    snimky = []
    for i in range(4):
        cesta = SLOZKA / "grafika" / f"{jmeno}_{i}.png"
        snimky.append(pygame.image.load(cesta).convert_alpha())
    return snimky


def nacti_mistnost(cislo, dlazdice):
    """Řetězce změníme na obrázek místnosti a obdélníky pro pravidla."""
    pozadi = pygame.Surface((SIRKA, VYSKA))
    pozadi.fill((8, 19, 27))
    pygame.draw.rect(pozadi, (38, 62, 70), (116, 128, 1048, 600), border_radius=16)
    zdi = []
    desky = {}
    for radek, znaky in enumerate(UROVNE[cislo]["mapa"]):
        for sloupec, znak in enumerate(znaky):
            rect = pygame.Rect(MAPA_X + sloupec * DLAZDICE,
                               MAPA_Y + radek * DLAZDICE, DLAZDICE, DLAZDICE)
            pozadi.blit(dlazdice[0], rect)
            if znak == "#":
                pozadi.blit(dlazdice[1], rect)
                zdi.append(rect)
            elif znak == "S":
                start = rect.center
            elif znak in "AB":
                pozadi.blit(dlazdice[2], rect)
                desky[znak] = rect.inflate(-20, -20)
            elif znak == "D":
                dvere = rect
            elif znak == "E":
                vychod = rect.inflate(-12, -12)
    return pozadi, zdi, start, desky, dvere, vychod


def main():
    # 3. INICIALIZACE A GRAFIKA – každý soubor leží uvnitř této složky.
    pygame.init()
    obrazovka = pygame.display.set_mode((SIRKA, VYSKA))
    pygame.display.set_caption("Ozvěny času | pygame-ce workshop")
    clock = pygame.time.Clock()
    male = pygame.font.Font(None, 23)
    normalni = pygame.font.Font(None, 28)
    velke = pygame.font.Font(None, 40)
    titulek = pygame.font.Font(None, 86)
    fonty = (male, normalni, velke, titulek)
    dlazdice = []
    for jmeno in ("podlaha", "zed", "deska", "dvere"):
        cesta = SLOZKA / "grafika" / f"{jmeno}.png"
        dlazdice.append(pygame.image.load(cesta).convert())
    snimky = nacti_snimky("hrac")
    snimky_ozveny = nacti_snimky("ozvena")
    for snimek in snimky_ozveny:
        snimek.set_alpha(170)
    zari = vytvor_zari()

    # 4. POSTAVY, SKUPINA A STAV. Historie je seznam pětic hodnot.
    cislo_urovne = 0
    pozadi, zdi, start, desky, dvere, vychod = nacti_mistnost(cislo_urovne, dlazdice)
    hrac = Hrac(snimky, start)
    ozvena = None
    postavy = pygame.sprite.Group(hrac)
    historie = []
    cas_zaznamu = 0
    # Fáze rozlišuje přípravu, záznam a přehrávání.
    faze = "priprava"
    # Stav hry určuje menu, hraní, pauzu nebo výsledek.
    stav_hry = "menu"
    dvere_otevrene = False
    cas_sepnuti = 0
    stisknute = {"A": False, "B": False}
    ukaz_data = False
    hlavni_tlacitko = pygame.Rect(196, 530, 350, 56)
    druhe_tlacitko = pygame.Rect(196, 603, 350, 52)
    tlacitka = (hlavni_tlacitko, druhe_tlacitko)
    running = True

    # 5. HERNÍ SMYČKA: EVENT → UPDATE → RENDER.
    while running:
        dt = min(clock.tick(FPS) / 1000, 0.04)
        # Akce je jednorázový povel z událostí pro tento průchod smyčkou.
        akce = ""
        ztrata_fokusu = False

        # EVENT – událost zvolí akci, kterou provedeme pod tímto cyklem.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if stav_hry == "hra":
                        stav_hry = "pauza"
                    elif stav_hry == "pauza":
                        stav_hry = "hra"
                    elif stav_hry == "menu":
                        running = False
                    else:
                        stav_hry = "menu"
                elif event.key == pygame.K_RETURN:
                    if stav_hry == "pauza":
                        stav_hry = "hra"
                    elif stav_hry == "uroven_hotova":
                        akce = "dalsi"
                    elif stav_hry in ("menu", "vyhra"):
                        akce = "nova"
                elif event.key == pygame.K_r and stav_hry in ("hra", "pauza"):
                    akce = "restart"
                elif event.key == pygame.K_SPACE and stav_hry == "hra":
                    akce = "prehrat" if faze == "zaznam" else "nahrat"
                elif event.key == pygame.K_F1:
                    ukaz_data = not ukaz_data
            elif event.type == pygame.WINDOWFOCUSLOST:
                ztrata_fokusu = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if stav_hry != "hra" and hlavni_tlacitko.collidepoint(event.pos):
                    if stav_hry == "pauza":
                        stav_hry = "hra"
                    else:
                        akce = "dalsi" if stav_hry == "uroven_hotova" else "nova"
                elif stav_hry != "hra" and druhe_tlacitko.collidepoint(event.pos):
                    if stav_hry == "menu":
                        running = False
                    else:
                        stav_hry = "menu"

        if akce in ("nova", "dalsi", "restart"):
            if akce == "nova":
                cislo_urovne = 0
            elif akce == "dalsi":
                cislo_urovne += 1
            pozadi, zdi, start, desky, dvere, vychod = nacti_mistnost(cislo_urovne, dlazdice)
            stav_hry = "hra"

        if akce in ("nova", "dalsi", "restart", "nahrat"):
            hrac = Hrac(snimky, start)
            ozvena = None
            postavy = pygame.sprite.Group(hrac)
            historie = []
            cas_zaznamu = 0
            faze = "priprava"
            dvere_otevrene = False
            cas_sepnuti = 0
            if akce == "nahrat":
                faze = "zaznam"
                historie.append((0, hrac.pozice.x, hrac.pozice.y, hrac.smer, hrac.snimek))

        if ztrata_fokusu and stav_hry == "hra":
            stav_hry = "pauza"

        # UPDATE – čas záznamu i ozvěny při pauze stojí.
        if stav_hry == "hra":
            dokoncit_zaznam = akce == "prehrat" and len(historie) > 1
            prekazky = zdi if dvere_otevrene else zdi + [dvere]
            if not dokoncit_zaznam:
                krok = dt
                if faze == "zaznam":
                    krok = min(dt, DELKA_ZAZNAMU - cas_zaznamu)
                hrac.update(krok, pygame.key.get_pressed(), prekazky)
                if faze == "zaznam" and krok > 0:
                    cas_zaznamu += krok
                    historie.append((cas_zaznamu, hrac.pozice.x, hrac.pozice.y,
                                     hrac.smer, hrac.snimek))
                    dokoncit_zaznam = cas_zaznamu >= DELKA_ZAZNAMU

            if dokoncit_zaznam:
                ozvena = Ozvena(snimky_ozveny, historie)
                hrac = Hrac(snimky, start)
                postavy = pygame.sprite.Group(ozvena, hrac)
                faze = "prehravani"
            elif ozvena is not None:
                ozvena.update(dt)

            for jmeno, deska in desky.items():
                stisknute[jmeno] = deska.collidepoint(hrac.pozice)
                if ozvena is not None and deska.collidepoint(ozvena.pozice):
                    stisknute[jmeno] = True

            # Obě desky musí být stisknuté současně. Dveře pak zůstanou otevřené.
            if faze == "prehravani" and all(stisknute.values()):
                cas_sepnuti = min(DOBA_SEPNUTI, cas_sepnuti + dt)
                if cas_sepnuti >= DOBA_SEPNUTI:
                    dvere_otevrene = True
            elif not dvere_otevrene:
                cas_sepnuti = 0
            if dvere_otevrene and vychod.collidepoint(hrac.pozice):
                stav_hry = "vyhra" if cislo_urovne == len(UROVNE) - 1 else "uroven_hotova"

        # RENDER – místnost je připravený obrázek, měnící se prvky kreslíme navrch.
        obrazovka.blit(pozadi, (0, 0))
        pygame.draw.circle(obrazovka, (119, 157, 163), start, 20, width=2)
        pygame.draw.circle(obrazovka, (119, 157, 163), start, 5)
        if len(historie) > 1:
            # Řidší body jsou jen pro kreslení; historie pro přehrávání zůstává úplná.
            body = []
            for cas, x, y, smer, snimek in historie[::6]:
                body.append((x, y))
            cas, x, y, smer, snimek = historie[-1]
            body.append((x, y))
            barva_trasy = (103, 160, 159) if ozvena else (161, 126, 82)
            pygame.draw.lines(obrazovka, barva_trasy, False, body, 2)
        for jmeno, deska in desky.items():
            barva = TYRKYSOVA if stisknute[jmeno] else ZLATA
            if stisknute[jmeno]:
                obrazovka.blit(zari, (deska.centerx - 50, deska.centery - 50))
            pygame.draw.rect(obrazovka, barva, deska, width=2, border_radius=7)
            text(obrazovka, normalni, jmeno, deska.centerx, deska.y + 11, barva, True)
        if dvere_otevrene:
            pygame.draw.rect(obrazovka, TYRKYSOVA, dvere.inflate(-8, -4), width=3, border_radius=5)
        else:
            obrazovka.blit(dlazdice[3], dvere)
        pygame.draw.rect(obrazovka, (31, 86, 88), vychod, border_radius=10)
        pygame.draw.rect(obrazovka, TYRKYSOVA, vychod, width=2, border_radius=10)
        text(obrazovka, velke, ">", vychod.centerx, vychod.y + 7, TYRKYSOVA, True)
        text(obrazovka, male, "EXIT", vychod.centerx, vychod.bottom + 4, TYRKYSOVA, True)
        for postava in postavy:
            pygame.draw.ellipse(obrazovka, (15, 34, 39), (postava.pozice.x - 16, postava.pozice.y + 3, 32, 12))
        if ozvena is not None:
            obrazovka.blit(zari, ozvena.pozice - (50, 50))
            text(obrazovka, male, "OZVĚNA", ozvena.rect.centerx, ozvena.rect.top - 20, TYRKYSOVA, True)
        postavy.draw(obrazovka)

        # Rozhraní: místnost vlevo, fáze a časová osa vpravo.
        text(obrazovka, male, "19 / LABORATOŘ ČASU", 128, 20, TYRKYSOVA)
        text(obrazovka, velke, UROVNE[cislo_urovne]["nazev"], 128, 46)
        text(obrazovka, male, f"MÍSTNOST {cislo_urovne + 1} / {len(UROVNE)}", 128, 94, TLUMENA)
        if faze == "priprava":
            nadpis, barva_faze = "01  PŘIPRAV SI CESTU", ZLATA
            rada = "MEZERNÍK: návrat na start a začátek záznamu"
            cas_osy = 0
        elif faze == "zaznam":
            nadpis, barva_faze = "02  NAHRÁVÁŠ SVOU MINULOST", CERVENA
            rada = "Dojdi na A. MEZERNÍK ukončí záznam."
            cas_osy = cas_zaznamu
        else:
            nadpis, barva_faze = "03  SPOLUPRACUJ S OZVĚNOU", TYRKYSOVA
            rada = "Dojdi na B. Ozvěna na konci své cesty zůstane."
            cas_osy = ozvena.cas
        if dvere_otevrene:
            rada = "Dveře jsou odemčené. Projdi vpravo do východu."
        text(obrazovka, normalni, nadpis, 660, 21, barva_faze)
        text(obrazovka, male, rada, 660, 52, BILA)
        pygame.draw.rect(obrazovka, (40, 66, 76), (660, 84, 340, 8), border_radius=4)
        pygame.draw.rect(obrazovka, barva_faze, (660, 84, round(340 * cas_osy / DELKA_ZAZNAMU), 8), border_radius=4)
        text(obrazovka, male, f"{cas_osy:04.1f} / {DELKA_ZAZNAMU}.0 s", 1020, 78, barva_faze)
        for i, jmeno in enumerate(("A", "B")):
            barva = TYRKYSOVA if stisknute[jmeno] else TLUMENA
            text(obrazovka, male, jmeno + ("  STISKNUTO" if stisknute[jmeno] else "  ČEKÁ"), 660 + i * 150, 104, barva)
        stav_dveri = "ODEMČENO" if dvere_otevrene else f"SOUBĚH {cas_sepnuti:.1f} / {DOBA_SEPNUTI} s"
        text(obrazovka, male, stav_dveri, 980, 104, TYRKYSOVA if dvere_otevrene else TLUMENA)
        text(obrazovka, normalni, UROVNE[cislo_urovne]["napoveda"], 128, 740)
        text(obrazovka, male, "WASD / šipky  pohyb     MEZERNÍK  záznam     R  reset místnosti     ESC  pauza     F1  data", 128, 772, TLUMENA)

        if ukaz_data:
            if stav_hry == "hra":
                zobrazene_prekazky = prekazky
            else:
                zobrazene_prekazky = zdi
            for prekazka in zobrazene_prekazky:
                pygame.draw.rect(obrazovka, (197, 109, 99), prekazka, width=1)
            for postava in postavy:
                pygame.draw.rect(obrazovka, TYRKYSOVA, postava.telo, width=1)
            panel(obrazovka, pygame.Rect(148, 154, 650, 72))
            index = ozvena.index if ozvena else 0
            text(obrazovka, male, f"historie: {len(historie)} vzorků    index ozvěny: {index}    fáze: {faze}", 164, 166)
            text(obrazovka, male, "vzorek = (čas, x, y, směr, snímek)    |    poloha hráče: " + f"({hrac.pozice.x:.0f}, {hrac.pozice.y:.0f})", 164, 194, TLUMENA)

        if stav_hry != "hra":
            kresli_menu(obrazovka, stav_hry, cislo_urovne, len(UROVNE),
                        UROVNE[cislo_urovne]["myslenka"], fonty, tlacitka)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
