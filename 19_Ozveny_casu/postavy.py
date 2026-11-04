"""Hráč reaguje na klávesy. Ozvěna čte dříve uložené polohy hráče."""

import pygame


class Hrac(pygame.sprite.Sprite):
    def __init__(self, frames, pozice):
        super().__init__()
        self.frames = frames
        self.frames_vlevo = [pygame.transform.flip(f, True, False) for f in frames]
        self.image = frames[0]
        self.pozice = pygame.Vector2(pozice)
        self.rychlost = 210
        self.smer = 1
        self.snimek = 0
        self.cas_animace = 0
        self.pohyb = False

        # Malé tělo u nohou slouží pro kolize. Obrázek může přesahovat nad zeď.
        self.telo = pygame.Rect(0, 0, 28, 24)
        self.telo.center = self.pozice
        self.rect = self.image.get_rect(midbottom=self.pozice + (0, 10))

    def update(self, dt, keys, prekazky):
        smer = pygame.Vector2(0, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            smer.x += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            smer.x -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            smer.y += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            smer.y -= 1
        if smer.length() > 0:
            # Chůze šikmo má stejnou rychlost jako chůze rovně.
            smer = smer.normalize()
        if smer.x != 0:
            self.smer = 1 if smer.x > 0 else -1

        puvodni_pozice = self.pozice.copy()

        # Nejdříve vyřešíme vodorovný pohyb, pak svislý.
        # Díky tomu lze podél zdi klouzat, i když míříme šikmo do ní.
        self.pozice.x += smer.x * self.rychlost * dt
        self.telo.centerx = round(self.pozice.x)
        for prekazka in prekazky:
            if self.telo.colliderect(prekazka):
                if smer.x > 0:
                    self.telo.right = prekazka.left
                    self.pozice.x = self.telo.centerx
                elif smer.x < 0:
                    self.telo.left = prekazka.right
                    self.pozice.x = self.telo.centerx

        self.pozice.y += smer.y * self.rychlost * dt
        self.telo.centery = round(self.pozice.y)
        for prekazka in prekazky:
            if self.telo.colliderect(prekazka):
                if smer.y > 0:
                    self.telo.bottom = prekazka.top
                    self.pozice.y = self.telo.centery
                elif smer.y < 0:
                    self.telo.top = prekazka.bottom
                    self.pozice.y = self.telo.centery

        self.pohyb = self.pozice != puvodni_pozice
        if self.pohyb:
            self.cas_animace += dt
        else:
            self.cas_animace = 0
        self.snimek = int(self.cas_animace * 8) % len(self.frames)
        if self.smer == 1:
            self.image = self.frames[self.snimek]
        else:
            self.image = self.frames_vlevo[self.snimek]
        self.rect = self.image.get_rect(midbottom=self.pozice + (0, 10))


class Ozvena(pygame.sprite.Sprite):
    def __init__(self, frames, historie):
        super().__init__()

        # Tyrkysové obrázky jsou připravené předem, načítá je main.py.
        self.frames = frames
        self.frames_vlevo = [
            pygame.transform.flip(f, True, False) for f in self.frames
        ]

        # Jeden záznam: (čas od začátku, x, y, směr, číslo obrázku).
        # První záznam vzniká v čase 0, další postupně přidává main.py.
        self.historie = historie.copy()
        self.cas = 0
        self.index = 0
        self.hotovo = False
        self.pozice = pygame.Vector2(historie[0][1], historie[0][2])
        self.smer = historie[0][3]
        self.snimek = historie[0][4]
        self.telo = pygame.Rect(0, 0, 28, 24)
        self.update(0)

    def update(self, dt):
        self.cas = min(self.cas + dt, self.historie[-1][0])

        # Najdeme poslední záznam, jehož čas už nastal.
        while (
            self.index + 1 < len(self.historie)
            and self.historie[self.index + 1][0] <= self.cas
        ):
            self.index += 1

        cas, x, y, self.smer, self.snimek = self.historie[self.index]
        self.pozice = pygame.Vector2(x, y)
        self.hotovo = self.index == len(self.historie) - 1

        if not self.hotovo:
            dalsi_cas, dalsi_x, dalsi_y, _, _ = self.historie[self.index + 1]
            # Při jiném FPS plynule dopočítáme polohu mezi dvěma záznamy.
            podil = (self.cas - cas) / (dalsi_cas - cas)
            self.pozice = self.pozice.lerp((dalsi_x, dalsi_y), podil)

        # Na konci ozvěna stojí na poslední poloze a dál může držet tlačítko.
        # Nepočítá znovu pohyb ani kolize: pouze přehrává uložená data.
        if self.smer == 1:
            self.image = self.frames[self.snimek]
        else:
            self.image = self.frames_vlevo[self.snimek]
        self.telo.center = self.pozice
        self.rect = self.image.get_rect(midbottom=self.pozice + (0, 10))
