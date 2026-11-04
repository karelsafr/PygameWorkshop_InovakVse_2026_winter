# Grafika hry Maják v mlze

Dva původní obrázky byly vytvořeny pro tuto hru vestavěným nástrojem Imagegen dne 30. 10. 2026. Nebyl použit externí balík grafiky. Pro předání studentům jsou z nich připravené PNG v konečné velikosti: jedno pozadí a osm animačních snímků. Hra je už jen načítá, bez ořezávání a změny velikosti. Písmo poskytuje pygame-ce (`pygame.font.Font(None, ...)`). Světlo, mlha, kruh bezpečí a rozhraní se kreslí v pygame; složitější grafické funkce jsou ve `vykresleni.py`.

Příprava použila přesně stejné oříznutí a zmenšení jako původní hra, takže výsledné pixely postav a pozadí zůstaly stejné. Původní podklady jsou zachované v pracovním archivu projektu `.build/zjednoduseni/pred/18_Majak_v_mlze/grafika/`; k hraní ani předání této složky nejsou potřeba. Přesná původní zadání následují níže.

## Pobrezi.png

Herní soubor: `grafika/pobrezi.png`, připravený na 1280 × 800 px. Pozadí s otevřenou pláží a majákem; bez postav a uživatelského rozhraní.

Zadání nástroji:

```text
Use case: stylized-concept
Asset type: production background for an actual playable 2D pygame game, landscape 16:10, ideally1280x800.
Create the complete background painting for "Maják v mlze", a cozy atmospheric lighthouse rescue game. High-quality hand-painted 2D environment, elevated orthographic TOP DOWN view with slight front faces of architecture, consistent readable game perspective, NO characters, NO text, NO UI, no baked circular lantern light, no thick fog covering gameplay.
Composition is FUNCTIONAL and mandatory. Large OPEN FLAT rectangular-ish sandy promenade/beach takes nearly the entire central and lower image, from x7% to93% and y29% to85%. This whole rectangle must be visibly connected WALKABLE SAND, free of obstacles: no large rocks, bushes, fences, water, props, holes or buildings anywhere inside it. Sparse fine sand texture and a few flat pebbles only. This large open area is where eight people and player will move.
Place one beautiful small coastal lighthouse at upper right, centered x85%, building footprint entirely ABOVE y29%, tower reaches near top of image. Cream stone lighthouse with ochre/copper dome and warm windows, attached tiny keeper cottage, entrance faces down toward the empty beach. A gentle sand approach leads from its door into open beach; no fences obstructing it.
Surround OUTSIDE the open rectangle with rocky navy-blue sea, carefully painted foam at image edges/bottom strip, a few tasteful coastal rocks at extreme left and upper edge, dark grasses only in outer boundary, cold indigo teal nighttime water, rich but subdued twilight colors. Edge silhouette should frame gameplay naturally. Foreground sea only below y88%; rocks on left only x<6%; rocks on right only x>94%. Leave upper-left region dark for an eventual title overlay, although deliver NO typography.
Mood calm mysterious blue-hour coastal night. Open sand is muted warm gray/beige lit by moonlight, sufficiently bright to distinguish small sprites, detailed natural surface, handcrafted indie game art, soft shadows, coherent shapes, elegant restrained contrast. Lighthouse has golden warm glow but no giant bloom obscuring detail. No other buildings. No perspective horizon, no isometric diamond island, no cinematic camera. Entire image filled, no borders. The walkable area must remain open and wide.
```

## Snímky postav

Původním výstupem byl průhledný atlas `postavy.png` se dvěma řadami po čtyřech animačních snímcích. Horní řada obsahovala strážce, spodní trosečníka. Z atlasu byly předem vyříznuté jednotlivé snímky, oříznuté průhledné okraje a sjednocená výška na 62 px. Studentům se předávají připravené soubory `grafika/strazce_0.png` až `strazce_3.png` a `grafika/trosecnik_0.png` až `trosecnik_3.png`.

Zadání nástroji:

```text
Use case: stylized-concept
Asset type: actual production SPRITE SHEET for 2D top-down lighthouse rescue game. TRANSPARENT background with real alpha.
A precise regular grid of EIGHT full-body character sprites: TWO ROWS and FOUR COLUMNS, equal cells, ideally overall1024x512. No text, no labels, no gridlines, no checkerboard painted into image. All figures isolated with large transparent margins, centered in each cell, feet aligned horizontally within each row. Same camera, same body scale, same light direction, same illustrative detail. Render clean highly readable hand-painted game sprites designed to appear around55pixels tall in game, generous silhouettes and simple details, slightly oversized head, elevated top-down 3/4 viewpoint facing to the RIGHT. Not pixel art, not photorealistic, not 3D render.
ROW ONE: identical lighthouse keeper wearing warm YELLOW hooded raincoat, brown boots, cream trousers, face partly seen side-on. Small warm glowing brass lantern held in right hand beside body. Exactly four animation frames of a walk cycle: neutral feet close, left foot forward, passing pose, right foot forward. Keep lantern and body dimensions identical. No ground plane, no large shadow. Subtle amber lantern glass but no huge glow halo.
ROW TWO: identical rescued sailor in dark NAVY coat, cream-and-blue striped shirt, knit blue cap, brown boots, small brown backpack. Exactly four matching walking animation frames neutral/left/passing/right. Same perspective and body height as keeper. Sailor carries NO lantern.
Whole limbs and hats contained inside each cell. Characters look like sympathetic adult figures of a refined cozy coastal story game. Opaque colors within sprites and real transparent background. No scenery or objects besides the personal lantern and backpack. Ensure8sprites exactly and uniform evenly spaced layout.
```

