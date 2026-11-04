"""Maják v mlze – samostatná hra navazující na workshopovou šablonu."""

from pathlib import Path
import math
import pygame

from postavy import Strazce, Trosecnik, STAV_ZACHRANENY
from vykresleni import (
    BILA, TLUMENA, ZLATA, text, panel, vytvor_zari, vytvor_mlhu,
    kresli_noc, kresli_menu,
)


# 1. KONSTANTY – pravidla hry upravujeme na jednom místě.
SIRKA, VYSKA = 1280, 800
FPS = 60
DELKA_NOCI = 180
VYDRZ_LUCERNY = 28  # sekund mimo maják při plném nabití
RYCHLOST_DOBIJENI = 35  # procent za sekundu
DOSAH_SVETLA = 150
BEZPECI = (1080, 365)
POLOMER_BEZPECI = 75
HRANICE = pygame.Rect(100, 330, 1080, 330)  # kam mohou vstoupit nohy postav
START_HRACE = (1020, 380)
MISTA_TROSECNIKU = [
    (180, 365), (350, 410), (540, 350), (745, 420),
    (175, 590), (400, 610), (650, 590), (875, 590),
]
SLOZKA = Path(__file__).parent
BARVY_STAVU = {
    "ztraceny": (168, 194, 214), "nasleduje": (136, 225, 191),
    "vystraseny": (255, 153, 127), "zachraneny": ZLATA,
}
NAZVY_STAVU = {
    "ztraceny": "ČEKÁ", "nasleduje": "NÁSLEDUJE",
    "vystraseny": "BOJÍ SE", "zachraneny": "V BEZPEČÍ",
}


# 2. NAČTENÍ OBRÁZKŮ A VYTVOŘENÍ POSTAV.
def nacti_snimky(jmeno):
    """Čtyři PNG už mají hotovou velikost; stačí je načíst v pořadí."""
    snimky = []
    for cislo in range(4):
        cesta = SLOZKA / "grafika" / f"{jmeno}_{cislo}.png"
        snimky.append(pygame.image.load(cesta).convert_alpha())
    return snimky


def nova_hra(snimky_hrace, snimky_lidi):
    hrac = Strazce(snimky_hrace, START_HRACE, HRANICE)
    lide = pygame.sprite.Group()
    for cislo, misto in enumerate(MISTA_TROSECNIKU):
        lide.add(Trosecnik(snimky_lidi, misto, HRANICE, cislo))
    vsechny_postavy = pygame.sprite.Group(hrac, *lide)
    return hrac, lide, vsechny_postavy


def main():
    # 3. START PYGAME A GRAFIKA – vše hledáme vedle tohoto souboru.
    pygame.init()
    obrazovka = pygame.display.set_mode((SIRKA, VYSKA))
    pygame.display.set_caption("Maják v mlze | pygame-ce workshop")
    clock = pygame.time.Clock()
    male = pygame.font.Font(None, 23)
    normalni = pygame.font.Font(None, 28)
    velke = pygame.font.Font(None, 42)
    titulek = pygame.font.Font(None, 94)
    pozadi = pygame.image.load(SLOZKA / "grafika" / "pobrezi.png").convert()
    snimky_hrace = nacti_snimky("strazce")
    snimky_lidi = nacti_snimky("trosecnik")
    zare = vytvor_zari(DOSAH_SVETLA)

    mlha = vytvor_mlhu()

    # 4. POSTAVY, SKUPINY A STAV HRY.
    hrac, lide, vsechny_postavy = nova_hra(snimky_hrace, snimky_lidi)
    stav_hry = "menu"
    energie = 100
    zbyva = DELKA_NOCI
    lucerna_zapnuta = True
    ukaz_stavy = False
    cas_obrazu = 0
    pocet_zachranenych = 0
    zprava = ""
    cas_zpravy = 0
    hlavni_tlacitko = pygame.Rect(76, 563, 300, 58)
    druhe_tlacitko = pygame.Rect(76, 638, 300, 48)
    running = True

    # 5. HERNÍ SMYČKA: EVENT → UPDATE → RENDER.
    while running:
        # Jeden herní krok má nejvýše 50 ms; po prodlevě nedohání celý skutečný čas.
        dt = min(clock.tick(FPS) / 1000, 0.05)
        cas_obrazu += dt
        spustit = False

        # EVENT – jednorázové stisky a tlačítka.
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
                    elif stav_hry != "hra":
                        spustit = True
                elif event.key == pygame.K_r:
                    spustit = True
                elif event.key == pygame.K_SPACE and stav_hry == "hra":
                    lucerna_zapnuta = not lucerna_zapnuta
                elif event.key == pygame.K_F1:
                    ukaz_stavy = not ukaz_stavy
            elif event.type == pygame.WINDOWFOCUSLOST and stav_hry == "hra":
                stav_hry = "pauza"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and stav_hry != "hra":
                if hlavni_tlacitko.collidepoint(event.pos):
                    if stav_hry == "pauza":
                        stav_hry = "hra"
                    else:
                        spustit = True
                elif druhe_tlacitko.collidepoint(event.pos):
                    if stav_hry == "menu":
                        running = False
                    else:
                        stav_hry = "menu"

        # Klávesa i tlačítko spustí novou hru stejným blokem po zpracování událostí.
        if spustit:
            hrac, lide, vsechny_postavy = nova_hra(snimky_hrace, snimky_lidi)
            energie = 100
            zbyva = DELKA_NOCI
            lucerna_zapnuta = True
            pocet_zachranenych = 0
            zprava = "Přibliž se k trosečníkům. Ve světle tě začnou následovat."
            cas_zpravy = 6
            stav_hry = "hra"

        # UPDATE – při pauze se tato část vůbec neprovádí.
        v_bezpeci = hrac.pozice.distance_to(BEZPECI) <= POLOMER_BEZPECI
        if stav_hry == "hra":
            hrac.update(dt, pygame.key.get_pressed())
            v_bezpeci = hrac.pozice.distance_to(BEZPECI) <= POLOMER_BEZPECI
            if v_bezpeci:
                energie = min(100, energie + RYCHLOST_DOBIJENI * dt)
            elif lucerna_zapnuta:
                energie = max(0, energie - 100 / VYDRZ_LUCERNY * dt)

            sviti = lucerna_zapnuta and energie > 0
            lide.update(dt, hrac, sviti, DOSAH_SVETLA, BEZPECI, POLOMER_BEZPECI)
            zachraneno = sum(clovek.stav == STAV_ZACHRANENY for clovek in lide)
            if zachraneno > pocet_zachranenych:
                zprava = f"Další člověk v bezpečí! Zachráněno {zachraneno} z {len(lide)}."
                cas_zpravy = 3
            pocet_zachranenych = zachraneno
            cas_zpravy = max(0, cas_zpravy - dt)
            zbyva = max(0, zbyva - dt)
            if zachraneno == len(lide):
                stav_hry = "vyhra"
            elif zbyva == 0:
                stav_hry = "prohra"

        # RENDER – nejprve pláž, pak postavy, světlo a nakonec rozhraní.
        obrazovka.blit(pozadi, (0, 0))
        sviti = lucerna_zapnuta and energie > 0
        zona = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        pygame.draw.circle(zona, (247, 193, 88, 22), BEZPECI, POLOMER_BEZPECI)
        pygame.draw.circle(zona, (247, 193, 88, 125), BEZPECI, POLOMER_BEZPECI, 2)
        obrazovka.blit(zona, (0, 0))

        # Nižší postava na obrazovce překryje tu, která stojí za ní.
        for postava in sorted(vsechny_postavy, key=lambda p: p.rect.bottom):
            if postava in lide and postava.stav == STAV_ZACHRANENY:
                continue
            pygame.draw.ellipse(obrazovka, (44, 49, 51),
                                (postava.pozice.x - 16, postava.pozice.y - 4, 32, 8))
            obrazovka.blit(postava.image, postava.rect)

        kresli_noc(obrazovka, hrac.pozice, sviti, zare, BEZPECI, DOSAH_SVETLA)
        for i in range(3):
            x = (cas_obrazu * (10 + i * 3) + i * 490) % 1840 - 560
            obrazovka.blit(mlha, (x, 255 + i * 170))
        text(obrazovka, male, "BEZPEČÍ / DOBÍJENÍ", BEZPECI[0], BEZPECI[1] - 98, ZLATA, True)

        for clovek in lide:
            if clovek.stav == STAV_ZACHRANENY:
                continue
            barva = BARVY_STAVU[clovek.stav]
            pygame.draw.circle(obrazovka, barva, (clovek.rect.centerx, clovek.rect.top - 9), 4)
            if ukaz_stavy:
                text(obrazovka, male, NAZVY_STAVU[clovek.stav], clovek.rect.centerx,
                     clovek.rect.top - 34, barva, True)
        if ukaz_stavy:
            pygame.draw.rect(obrazovka, TLUMENA, HRANICE, 1)
            if sviti:
                pygame.draw.circle(obrazovka, ZLATA, hrac.pozice, DOSAH_SVETLA, 1)

        # HORNÍ LIŠTA – cíle a dvě skutečné herní veličiny.
        panel(obrazovka, pygame.Rect(24, 20, 1232, 78))
        text(obrazovka, male, "NOČNÍ HLÍDKA", 48, 34, ZLATA)
        text(obrazovka, normalni, "Maják v mlze", 48, 59)
        text(obrazovka, male, "ZACHRÁNĚNO", 365, 35, TLUMENA)
        text(obrazovka, normalni, f"{pocet_zachranenych} / {len(lide)}", 365, 59)
        text(obrazovka, male, "ČAS DO KONCE NOCI", 570, 35, TLUMENA)
        sekundy = math.ceil(zbyva)
        text(obrazovka, normalni, f"{sekundy // 60:02}:{sekundy % 60:02}", 570, 59)
        stav_lucerny = "DOBÍJENÍ" if v_bezpeci and energie < 100 else "LUCERNA"
        if not lucerna_zapnuta:
            stav_lucerny = "LUCERNA VYPNUTÁ"
        text(obrazovka, male, stav_lucerny, 855, 35, ZLATA)
        pygame.draw.rect(obrazovka, (44, 60, 70), (855, 64, 290, 8), border_radius=4)
        if energie > 0:
            pygame.draw.rect(obrazovka, ZLATA, (855, 64, round(290 * energie / 100), 8), border_radius=4)
        text(obrazovka, male, f"{round(energie)} %", 1170, 56)

        if stav_hry == "hra":
            panel(obrazovka, pygame.Rect(24, 735, 1232, 45), 235)
            text(obrazovka, male, "WASD / šipky  pohyb     SHIFT  pomalu     MEZERNÍK  lucerna", 45, 748)
            text(obrazovka, male, "F1  stavy postav     ESC  pauza     R  znovu", 830, 748, TLUMENA)
            if cas_zpravy > 0:
                panel(obrazovka, pygame.Rect(290, 115, 700, 40), 205)
                text(obrazovka, male, zprava, SIRKA // 2, 127, BILA, True)
            elif energie < 20:
                text(obrazovka, normalni, "Světlo slábne. Vrať se k majáku.", SIRKA // 2, 122, ZLATA, True)

        # MENU, PAUZA A VÝSLEDEK používají stejné dva obdélníky tlačítek.
        else:
            kresli_menu(obrazovka, stav_hry, pocet_zachranenych, sekundy,
                        (male, normalni, velke, titulek),
                        (hlavni_tlacitko, druhe_tlacitko))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
