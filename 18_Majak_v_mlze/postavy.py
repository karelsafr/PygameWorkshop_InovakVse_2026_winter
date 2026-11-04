"""Pohyb a stavy postav. Rozhraní a grafické efekty jsou ve vykresleni.py."""

import pygame


# Stav je obyčejný řetězec. Podle něj vybíráme chování trosečníka.
STAV_ZTRACENY = "ztraceny"
STAV_NASLEDUJE = "nasleduje"
STAV_VYSTRASENY = "vystraseny"
STAV_ZACHRANENY = "zachraneny"


def animuj(postava, dt):
    """Obě postavy používají stejný způsob střídání obrázků."""
    if postava.pohyb:
        postava.cas_animace += dt
    else:
        postava.cas_animace = 0

    snimek = int(postava.cas_animace * 8) % len(postava.frames)
    if postava.smer == 1:
        postava.image = postava.frames[snimek]
    else:
        postava.image = postava.frames_vlevo[snimek]

    # Pozice označuje nohy postavy, nikoli levý horní roh obrázku.
    # Desetinnou polohu drží pozice; Rect z ní jen určuje místo vykreslení.
    postava.rect = postava.image.get_rect(midbottom=postava.pozice)


class Strazce(pygame.sprite.Sprite):
    def __init__(self, frames, pozice, hranice):
        super().__init__()
        self.frames = frames
        self.frames_vlevo = [pygame.transform.flip(f, True, False) for f in frames]
        self.image = frames[0]
        self.pozice = pygame.Vector2(pozice)
        self.rect = self.image.get_rect(midbottom=self.pozice)
        self.hranice = hranice
        self.rychlost = 180
        self.pohyb = False
        self.smer = 1
        self.cas_animace = 0

    def update(self, dt, keys):
        smer = pygame.Vector2(0, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            smer.x += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            smer.x -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            smer.y += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            smer.y -= 1
        # Samostatné podmínky dovolí šikmý pohyb i vyrušení opačných směrů.
        self.pohyb = smer.length() > 0
        rychlost = self.rychlost
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            rychlost = 120  # Při doprovázení skupiny je vhodná pomalejší chůze.

        if self.pohyb:
            # Normalizace zajistí stejnou rychlost i při chůzi šikmo.
            self.pozice += smer.normalize() * rychlost * dt
            if smer.x != 0:
                self.smer = 1 if smer.x > 0 else -1

        self.pozice.x = max(self.hranice.left, min(self.pozice.x, self.hranice.right))
        self.pozice.y = max(self.hranice.top, min(self.pozice.y, self.hranice.bottom))
        animuj(self, dt)


class Trosecnik(pygame.sprite.Sprite):
    def __init__(self, frames, pozice, hranice, poradi):
        super().__init__()
        self.frames = frames
        self.frames_vlevo = [pygame.transform.flip(f, True, False) for f in frames]
        self.image = frames[0]
        self.pozice = pygame.Vector2(pozice)
        self.rect = self.image.get_rect(midbottom=self.pozice)
        self.hranice = hranice
        self.rychlost = 150
        self.pohyb = False
        self.smer = 1
        self.cas_animace = 0
        self.stav = STAV_ZTRACENY
        self.cas_strachu = 0
        # Pamatuje si, zda už někdy následoval; strach tuto informaci nemaže.
        self.sel_za_hracem = False

        # Každý míří k trochu jinému bodu, aby nestáli všichni na sobě.
        self.odstup = pygame.Vector2((poradi % 3 - 1) * 24, 26 + (poradi // 3) * 14)

    def update(self, dt, strazce, svetlo, dosah, bezpeci, polomer_bezpeci):
        self.pohyb = False
        if self.stav == STAV_ZACHRANENY:
            return

        # V bezpečí zachráníme i člověka, kterému právě zhasla lucerna.
        if self.sel_za_hracem and self.pozice.distance_to(bezpeci) <= polomer_bezpeci:
            self.stav = STAV_ZACHRANENY
            animuj(self, dt)
            return

        vzdalenost = self.pozice.distance_to(strazce.pozice)

        # 1. Přechody mezi stavy: co se právě změnilo v okolí postavy?
        if svetlo and vzdalenost <= dosah:
            self.stav = STAV_NASLEDUJE
            self.sel_za_hracem = True
        elif self.stav == STAV_NASLEDUJE:
            # Malá rezerva brání neustálému přepínání na hranici světla.
            if not svetlo or vzdalenost > dosah + 20:
                self.stav = STAV_VYSTRASENY
                self.cas_strachu = 2

        # 2. Chování podle aktuálního stavu.
        if self.stav == STAV_NASLEDUJE:
            cil = strazce.pozice + self.odstup
            smer = cil - self.pozice
            vzdalenost_do_cile = smer.length()
            if vzdalenost_do_cile > 4:
                krok = min(self.rychlost * dt, vzdalenost_do_cile)
                self.pozice += smer.normalize() * krok
                self.pohyb = True
                if smer.x != 0:
                    self.smer = 1 if smer.x > 0 else -1

        elif self.stav == STAV_VYSTRASENY:
            self.cas_strachu -= dt
            if self.cas_strachu <= 0:
                self.stav = STAV_ZTRACENY

        # Ztracený člověk čeká na místě. Hledání cesty v této ukázce není.
        self.pozice.x = max(self.hranice.left, min(self.pozice.x, self.hranice.right))
        self.pozice.y = max(self.hranice.top, min(self.pozice.y, self.hranice.bottom))

        # 3. Do bezpečné zóny mohl trosečník dojít i v tomto kroku.
        if self.sel_za_hracem and self.pozice.distance_to(bezpeci) <= polomer_bezpeci:
            self.stav = STAV_ZACHRANENY
            self.pohyb = False

        animuj(self, dt)
