# Grafika hry Ozvěny času

Dva původní rastrové obrázky byly vytvořeny vestavěným nástrojem **Imagegen** dne 30. 10. 2026 pro tento příklad. Nebyly převzaty z cizí sady. Níže jsou přesná zadání. Původní generované soubory zůstávají v pracovním archivu projektu; studentská složka obsahuje připravené obrázky v konečné velikosti.

- `grafika/podlaha.png`, `zed.png`, `deska.png`, `dvere.png`: čtyři dlaždice 64 × 64 px vyříznuté z původního atlasu 2 × 2.
- `grafika/hrac_0.png` až `hrac_3.png`: čtyři animační snímky na průhledném pozadí, oříznuté a zmenšené na výšku 52 px.
- `grafika/ozvena_0.png` až `ozvena_3.png`: stejné snímky předem obarvené tyrkysově. Hra při načtení pouze nastaví jejich celkovou průhlednost na 170 z 255.
- Výřezy, velikosti i barvy odpovídají původnímu načítání ve hře. Příprava proběhla jednorázově před předáním, aby studenti nemuseli v herním kódu řešit ořezávání a barevné operace. Nová grafika se při této úpravě negenerovala.
- Záře, značky A/B, start, východ, trasa, časová osa a rozhraní se kreslí přímo v pygame. Grafické pomůcky a nabídky jsou v `vykresleni.py`.
- `nahled.png` je snímek vykreslené hry, nikoli výtvarný návrh.

## Zadání atlasu

```text
Use case: stylized-concept
Asset type: PRODUCTION 2D GAME TILE ATLAS, FOUR square tiles arranged in an exact2x2 grid, overall square image. Every tile occupies exactly one quarter of the image, perfectly aligned, NO gutters, NO outside border, NO text, NO labels. Individual tiles must be readable at64x64 pixels.
Theme: abandoned retrofuturist time laboratory, refined hand-painted 2D game artwork, top-down orthographic camera. Dark petrol-blue steel, aged copper accents, restrained amber and turquoise light, tactile brushed metal and stone. This is a usable tile sheet, NOT a perspective scene, NO perspective horizon, no angled isometric view.
TOP LEFT quadrant: walkable FLOOR TILE. Flat desaturated blue-gray square steel/stone floor slab with subtle brushed texture, tiny bolts in corners and a soft narrow seam at all four edges. Mostly calm uncluttered center. No tall objects, no shadows of unseen objects, no cables across the middle. Moderately light floor so small orange player will show up.
TOP RIGHT quadrant: solid WALL / MACHINE BLOCK TILE. Top-down square dark-teal metal machine housing with clear thick raised copper-edged perimeter, two small subdued cyan status lamps, a couple of engraved industrial seams. Occupies entire square, clearly solid and nonwalkable. It must be tileable side-by-side into continuous walls, not an isolated chest sitting on a floor. Crisp 2D painted relief only.
BOTTOM LEFT quadrant: inactive PRESSURE PLATE TILE on EXACT SAME floor as top-left. A recessed heavy square copper pressure pad centered in the tile, covering60percent of width, beveled edges, dark unlit center and four small recessed light slots at corners. No letters or symbols. Make pad distinct and centered. It will light up via code. Keep the surrounding floor identical palette to top-left.
BOTTOM RIGHT quadrant: CLOSED DOOR TILE on same floor, square mechanical security hatch centered, dark copper vertical panels flanked by petrol-blue steel rails, thin restrained warm amber light strips indicating locked. Entire barrier is inside tile, fitswalltheme. No lettering. Top-down view, no upright 3D architectural scene.
Make all four tiles align exactly to mathematical halfwidth/halfheight boundaries, no whitespace. One coherent artist style. Opaque background. Keep major silhouettes strong and legible at64px.
```

## Zadání postavy

```text
Use case: stylized-concept
Asset type: PRODUCTION sprite sheet for actual 2D top-down puzzle game called Ozvěny času. TRUE transparent background.
Create exactly FOUR equal-sized full-body walking frames arranged in a single horizontal row of FOUR equal rectangular cells, landscape image. No text, no gridlines, no labels, no fake checkerboard. All sprites face RIGHT, all feet aligned to same horizontal baseline, same character scale and camera and lighting. Large transparent margin around each full figure, do not clip any part.
Character: sympathetic adult laboratory explorer wearing a warm AMBER/ORANGE padded work suit, cream chest panel, charcoal gloves and boots, small dark navy backpack, rounded copper-orange headgear with clearly visible pale cyan glass eye visor. Tiny blue time-device clipped to belt; no weapons. Slightly oversized head and compact readable silhouette, detailed hand-painted 2D indie-game aesthetic, top-down elevated 3/4 view so face and front sides can be seen but suitable to walk around a flat overhead tile map.
Frame1 neutral feetclose standing, frame2 left legforward walking, frame3 passingpose, frame4 right legforward walking. Natural subtle arm swing; identical outfit, head, backpack, colors and proportions in every cell. Designed to display around52pixels high in game, readable painterly forms with clean alpha edges. No large glow halos, no ground/shadow/scenery. Four sprites exactly, evenly spaced, no extra accessories outside each sprite. No photorealism, no pixel art, no3D rendering, no UI.
```

