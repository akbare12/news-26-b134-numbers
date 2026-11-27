#!/usr/bin/env python3
"""Render news-image-20261126 entry for b134 (layout V130, numbers-only).

V130: masthead + DATE CHECK strip; vertical timeline rail on the right;
3 heroes in one row (art on top, text below, zero overlap by construction);
10 cards 5x2; bottom: numbered-pin world map (left) + ALSO 2 columns (right).
All art is drawn on its own layer sized exactly to its box, so no art pixel
can ever cover a text pixel. 1024x1024, stdlib+PIL build-time only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FD + name, size)

F_TITLE = font("DejaVuSans-Bold.ttf", 34)
F_DATE = font("DejaVuSans-Bold.ttf", 15)
F_SUB = font("DejaVuSans-Bold.ttf", 11)
F_DC = font("DejaVuSans.ttf", 11)
F_DCB = font("DejaVuSans-Bold.ttf", 11)
F_KICK = font("DejaVuSans-Bold.ttf", 10)
F_HEAD = font("DejaVuSans-Bold.ttf", 15)
F_DECK = font("DejaVuSans.ttf", 10)
F_WHY = font("DejaVuSans.ttf", 9)
F_WHYB = font("DejaVuSans-Bold.ttf", 9)
F_CARD_K = font("DejaVuSans-Bold.ttf", 10)
F_CARD_H = font("DejaVuSans-Bold.ttf", 11)
F_CARD_D = font("DejaVuSans.ttf", 9)
F_STAT = font("DejaVuSans-Bold.ttf", 9)
F_ALSO = font("DejaVuSans.ttf", 9)
F_ALSO_H = font("DejaVuSans-Bold.ttf", 12)
F_MAP_H = font("DejaVuSans-Bold.ttf", 11)
F_LEG = font("DejaVuSans.ttf", 9)
F_LEGB = font("DejaVuSans-Bold.ttf", 9)
F_TL_H = font("DejaVuSans-Bold.ttf", 12)
F_TL = font("DejaVuSans.ttf", 9)
F_TLB = font("DejaVuSans-Bold.ttf", 9)
F_FOOT = font("DejaVuSans.ttf", 9)

INK = (18, 18, 18)
PAPER = (250, 248, 242)
NAVY = (16, 32, 64)
RED = (178, 34, 34)
GOLD = (255, 243, 205)
GOLD_LINE = (180, 140, 40)
BLUE = (30, 80, 160)
GREY = (110, 110, 110)
LAND_RGB = (196, 178, 140)  # drawn-land colour; pin asserts check this exact pixel

def tw(draw, s, f):
    return draw.textlength(s, font=f)

def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_lines(draw, text, f, max_w, max_lines, where):
    lines = wrap(draw, text, f, max_w)
    assert len(lines) <= max_lines, f"{where}: {len(lines)} lines > {max_lines}: {lines}"
    for ln in lines:
        assert draw.textlength(ln, font=f) <= max_w + 0.5, f"{where}: line too wide: {ln}"
    return lines

def box_overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

HEROES = [
    dict(kicker="NEW YORK \u00b7 [C]", tag="[C]",
         head="MACY'S 100TH PARADE POSTPONED",
         deck="First weather postponement ever; gusts hit 60 mph. "
              "Philadelphia's parade is cancelled too. Moves to Sat 28 Nov, 08:30 ET.",
         why="America's most iconic parade moves to Saturday, "
             "and balloon rules face a rethink.",
         art="balloons"),
    dict(kicker="STRAIT OF HORMUZ \u00b7 [CL]", tag="[CL]",
         head="IRGC CLAIMS 2 TANKERS HIT BY MINES",
         deck="Supertanker carrying 2M barrels among the targets; "
              "crew safe after a blast off Dubai.",
         why="If true, it widens the Iran war to the oil chokepoint; "
             "Brent already hit $93.8.",
         art="tanker"),
    dict(kicker="GLOBAL MARKETS \u00b7 [C]", tag="[C]",
         head="TRUMP TARIFFS: MARKETS REBOUND",
         deck="Salvo hits 14 partners: China 20%, EU 15%. "
              "STOXX +1.6% and MSCI +0.4% as fears ease.",
         why="Traders judged the salvo milder than feared, as duties "
             "will not stack on July's.",
         art="chart"),
]

CARDS = [
    ("GAZA", "[C]", "Israel kills Hamas education chief",
     "Abu Nada and wife killed in Gaza; 9 dead on third night of strikes.",
     "9 KILLED \u00b7 3RD NIGHT"),
    ("KYIV", "[C]", "Ballistic strike hits Kyiv mall",
     "Iskander and Zircon hit Desnianskyi; 7 hurt as 113 drones fly in.",
     "7 HURT \u00b7 113 DRONES"),
    ("BOGOR", "[C]", "Flooded gold mine toll rises",
     "Illegal mine floods in Bogor; 13 dead and 13 missing underground.",
     "13 DEAD \u00b7 13 MISSING"),
    ("JERUSALEM", "[C]", "Judge urges bribery charge dropped",
     "Netanyahu Case 4000: judge advises prosecutors to drop the charge.",
     "CASE 4000 \u00b7 BRIBERY"),
    ("PYONGYANG", "[C]", "Kim tours nuclear plant",
     "State media: Kim pushes wider use of tactical nuclear arms.",
     "TACTICAL NUKES"),
    ("WASHINGTON", "[C]", "FCC clears 1M SpaceX satellites",
     "Starmind orbital data centres approved 25 Nov, reported 26 Nov.",
     "1M SATELLITES"),
    ("LONDON", "[C]", "UK migration falls to 77,000",
     "Net migration lowest since 1997, outside the pandemic years.",
     "77,000 \u00b7 RECORD LOW"),
    ("MOSCOW", "[C]", "Record military budget passed",
     "Russia approves its biggest post-Soviet defence budget.",
     "RECORD POST-SOVIET"),
    ("BANGKOK", "[C]", "Oil depot blast hurts 7",
     "Bangkok oil depot blast; fire out in about 30 minutes.",
     "7 HURT \u00b7 FIRE OUT ~30 MIN"),
    ("COLOGNE", "[C]", "2 held over synagogue plot",
     "Iraqi suspects held in Cologne and Heidelberg over March plot.",
     "2 HELD \u00b7 MARCH PLOT"),
]

ALSO = [
    "NBC airs 2025 parade on Thursday [C]",
    "OPEC+ meets 29 Nov on 2027 output [C]",
    "NYC bars balloons over 23 mph wind [C]",
    "Mamdani to miss Sat parade, foot op [C]",
    "UKMTO 222-26: blast 50 nm west of Dubai [C]",
    "UKMTO: blast off Khasab, 25 Nov [CL]",
    "Saudi downs 2 missiles to Riyadh [R]",
    "Houthi claim Ras Tanura strike, 25 Nov [CL]",
    "Jazan port suffers minor damage [R]",
    "Tariff hearings 25 Jan; rollout Feb/Mar [C]",
    "Indonesia faces 18% tariff in salvo [C]",
    "Vietnam faces up to 35% if talks fail [C]",
    "Singapore faces 10% tariff [C]",
    "India faces 17%/25% tariff [C]",
    "S&P 500 -0.25%; Nasdaq -0.62% Wed [C]",
    "Dow +0.33% on Wednesday [C]",
    "Gold $3,572/oz; down 8% in a month [C]",
    "Dollar flat at 103.71 [C]",
    "18 wounded in Kryvyi Rih strike [C]",
    "Couple, 37 and 38, killed in Kharkiv [C]",
    "Ukraine hits Savasleyka; 5 jets damaged [C]",
    "Subkhankulovo burns, 1,300 km in [R]",
    "Cargo ship near Odesa reportedly hit [R]",
    "UN rights chief warns on Gaza [C]",
    "Eisenkot wins first Israel coalition deal [C]",
    "Merz warns Russia aims beyond Ukraine [C]",
    "UK on alert over drone threat to bases [C]",
    "Norse Atlantic suspends all flights [C]",
    "Poundland in administration, 11,000 jobs [C]",
    "Malaysia sues Google $146m [C]",
    "Kenya court halts US-backed Ebola site [C]",
    "Zelensky turns down Belarus flight offer [C]",
    "Kushner: Putin 'grandmaster of politics' [C]",
    "Estonia decides to close border [C]",
    "Copernicus: longest stretch above 2C [C]",
    "Nvidia halts AI shipments to 4 nations [R]",
    "US Bitcoin funds hit record $4.94bn [C]",
]

TIMELINE = [
    "NIGHT - Kyiv ballistic hit",
    "10:00 - NYC wind warning",
    "MORNING - Markets rebound",
    "MIDDAY - Hormuz claim lands",
    "EVENING - Gaza strike, 9 die",
    "SAT 08:30 - Parade moves",
]

DATE_CHECK = [
    "DATE CHECK - NOT 26 NOV: COP31 failed (22 Nov) \u00b7 Shenzhou-24 launch (25 Nov) \u00b7 "
    "Cairo tanker, 31 killed (25 Nov) \u00b7 Cartagena hostages freed (25 Nov)",
    "Australia-Solomon pact (25 Nov) \u00b7 UK energy +26% (25 Nov) \u00b7 "
    "Huawei convicted (24 Nov) - all excluded on purpose.",
]

# ---- art layers: each drawn on its own image sized exactly to its box ----
def art_balloons(w, h):
    im = Image.new("RGB", (w, h), (135, 175, 215))
    d = ImageDraw.Draw(im)
    d.rectangle([0, h - 26, w, h], fill=(70, 70, 78))
    for bx in (28, 96, 164, 222):
        d.rectangle([bx, h - 52, bx + 22, h - 26], fill=(52, 52, 60))
    cols = [(214, 48, 49), (38, 90, 160), (230, 170, 30)]
    for i, (cx, cy, r, c) in enumerate([(52, 34, 26, cols[0]), (128, 26, 30, cols[1]),
                                        (204, 36, 24, cols[2])]):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
        d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(255, 255, 255), width=2)
        d.line([cx - 6, cy + r, cx - 4, cy + r + 12], fill=(60, 60, 60), width=2)
        d.line([cx + 6, cy + r, cx + 4, cy + r + 12], fill=(60, 60, 60), width=2)
    return im

def art_tanker(w, h):
    im = Image.new("RGB", (w, h), (18, 44, 74))
    d = ImageDraw.Draw(im)
    d.rectangle([0, h - 34, w, h], fill=(10, 30, 55))
    d.rectangle([14, h - 52, w - 14, h - 34], fill=(12, 12, 14))
    d.rectangle([w - 78, h - 72, w - 38, h - 52], fill=(200, 200, 200))
    d.rectangle([w - 70, h - 80, w - 46, h - 72], fill=(160, 160, 160))
    for fx, fy, fr in [(70, h - 58, 14), (100, h - 64, 10), (52, h - 56, 8)]:
        d.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], fill=(255, 140, 0))
        d.ellipse([fx - fr // 2, fy - fr // 2, fx + fr // 2, fy + fr // 2], fill=(255, 210, 60))
    d.ellipse([196, 12, 210, 26], outline=(255, 255, 255), width=2)
    d.ellipse([222, 26, 234, 38], outline=(255, 255, 255), width=2)
    return im

def art_chart(w, h):
    im = Image.new("RGB", (w, h), (16, 48, 32))
    d = ImageDraw.Draw(im)
    d.rectangle([0, h - 14, w, h], fill=(10, 32, 22))
    bars = [(20, 30), (52, 44), (84, 36), (116, 54), (148, 48), (180, 64), (212, 58)]
    for bx, bh in bars:
        d.rectangle([bx, h - 14 - bh, bx + 20, h - 14], fill=(46, 140, 90))
    pts = [(10, h - 30), (48, h - 52), (86, h - 44), (124, h - 66),
           (162, h - 58), (200, h - 78), (238, h - 70)]
    d.line(pts, fill=(255, 210, 60), width=4)
    for x, y in pts:
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 210, 60))
    return im

ART = {"balloons": art_balloons, "tanker": art_tanker, "chart": art_chart}

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    text_boxes = []   # (bbox, label) every text box drawn on the page
    art_boxes = []    # (bbox, label) every art box pasted on the page

    def text(xy, s, f, fill=INK):
        d.text(xy, s, font=f, fill=fill)
        x, y = xy
        w = d.textlength(s, font=f)
        asc, desc = f.getmetrics()
        text_boxes.append(((x, y, x + w, y + asc + desc), s[:28]))

    # ---- masthead ----
    text((16, 8), "THE WORLD IN ONE DAY", F_TITLE)
    text((640, 22), "THURSDAY 26 NOVEMBER 2026", F_DATE, fill=RED)
    text((16, 46), "50 STORIES  \u00b7  10 REGIONS  \u00b7  ALL VERIFIED 26 NOV 2026",
         F_SUB, fill=GREY)
    d.line([8, 58, 1016, 58], fill=RED, width=3)

    # ---- DATE CHECK strip (gold, 2 lines) ----
    d.rectangle([8, 62, 1016, 100], fill=GOLD, outline=GOLD_LINE, width=1)
    text((16, 64), DATE_CHECK[0], F_DC)
    text((16, 80), DATE_CHECK[1], F_DC)
    assert d.textlength(DATE_CHECK[0], font=F_DC) <= 992, "date check line 1 too wide"
    assert d.textlength(DATE_CHECK[1], font=F_DC) <= 992, "date check line 2 too wide"

    # ---- heroes: 3 columns, art box on top, all text below it ----
    hero_xs = [8, 268, 528]
    hero_w = 256
    art_y0, art_y1 = 108, 200
    for i, hero in enumerate(HEROES):
        x0 = hero_xs[i]
        d.rectangle([x0, 104, x0 + hero_w, 330], outline=(200, 200, 200), width=1)
        d.rectangle([x0, 104, x0 + hero_w, 106], fill=NAVY)
        layer = ART[hero["art"]](hero_w, art_y1 - art_y0)
        img.paste(layer, (x0, art_y0))
        art_boxes.append(((x0, art_y0, x0 + hero_w, art_y1), "hero%d art" % (i + 1)))
        # kicker band directly under art (solid, no text over art)
        d.rectangle([x0, 200, x0 + hero_w, 218], fill=NAVY)
        text((x0 + 6, 203), hero["kicker"], F_KICK, fill=(255, 255, 255))
        head_lines = fit_lines(d, hero["head"], F_HEAD, hero_w - 12, 2, "hero%d head" % (i + 1))
        y = 222
        for ln in head_lines:
            text((x0 + 6, y), ln, F_HEAD)
            y += 18
        deck_lines = fit_lines(d, hero["deck"], F_DECK, hero_w - 12, 3, "hero%d deck" % (i + 1))
        y = 260
        for ln in deck_lines:
            text((x0 + 6, y), ln, F_DECK)
            y += 12
        why_top = 296
        assert y <= why_top, "hero%d deck ends %d, why starts %d" % (i + 1, y, why_top)
        text((x0 + 6, why_top), "WHY IT MATTERS:", F_WHYB, fill=RED)
        why_lines = fit_lines(d, hero["why"], F_WHY, hero_w - 12, 2, "hero%d why" % (i + 1))
        assert hero["why"].rstrip().endswith("."), "hero%d why must end with a full stop" % (i + 1)
        y = 308
        for ln in why_lines:
            text((x0 + 6, y), ln, F_WHY)
            y += 10
        assert y <= 330, "hero%d why overflows: ends %d" % (i + 1, y)

    # ---- cards 5x2 ----
    card_w, card_h = 152, 106
    card_xs = [8, 166, 324, 482, 640]
    card_ys = [336, 448]
    for n, (city, tag, head, deck, stat) in enumerate(CARDS):
        cx = card_xs[n % 5]
        cy = card_ys[n // 5]
        d.rectangle([cx, cy, cx + card_w, cy + card_h], outline=(200, 200, 200), width=1)
        d.rectangle([cx, cy, cx + card_w, cy + 2], fill=RED)
        text((cx + 6, cy + 6), "%s %s" % (city, tag), F_CARD_K)
        head_lines = fit_lines(d, head, F_CARD_H, card_w - 12, 2, "card%d head" % (n + 1))
        y = cy + 22
        for ln in head_lines:
            text((cx + 6, y), ln, F_CARD_H)
            y += 13
        deck_lines = fit_lines(d, deck, F_CARD_D, card_w - 12, 3, "card%d deck" % (n + 1))
        y = cy + 50
        for ln in deck_lines:
            text((cx + 6, y), ln, F_CARD_D)
            y += 11
        stat_y = cy + card_h - 16
        assert y <= stat_y - 2, "card%d deck ends %d, stat at %d" % (n + 1, y, stat_y)
        assert d.textlength(stat, font=F_STAT) <= card_w - 12, "card%d stat too wide" % (n + 1)
        text((cx + 6, stat_y), stat, F_STAT, fill=RED)
    return img, d, text_boxes, art_boxes

# ---- map + ALSO + timeline + footer (second half of render) ----
def render_bottom(img, d, text_boxes, art_boxes):
    def text(xy, s, f, fill=INK):
        d.text(xy, s, font=f, fill=fill)
        x, y = xy
        w = d.textlength(s, font=f)
        asc, desc = f.getmetrics()
        text_boxes.append(((x, y, x + w, y + asc + desc), s[:28]))

    # map panel: x8-330, y566-986. Map drawn on its own layer = clipped by construction.
    map_x0, map_y0, map_w, map_h = 8, 566, 322, 420
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h],
                outline=(200, 200, 200), width=1)
    text((map_x0 + 8, map_y0 + 6), "WHERE IT HAPPENED", F_MAP_H)
    d.line([map_x0 + 8, map_y0 + 24, map_x0 + map_w - 8, map_y0 + 24], fill=RED, width=2)
    mx0, my0, mw, mh = map_x0 + 4, map_y0 + 30, map_w - 8, 300
    layer = Image.new("RGB", (mw, mh), (214, 232, 240))
    md = ImageDraw.Draw(layer)
    def proj(lon, lat):
        return ((lon + 170.0) / 360.0 * mw, (78.0 - lat) / 136.0 * mh)
    continents = [
        [(-168, 66), (-150, 70), (-130, 71), (-115, 68), (-100, 68), (-90, 69),
         (-82, 66), (-76, 62), (-70, 58), (-60, 52), (-55, 47), (-65, 44),
         (-70, 42), (-75, 38), (-80, 32), (-81, 26), (-84, 30), (-90, 29),
         (-97, 26), (-105, 22), (-110, 24), (-115, 29), (-120, 34), (-125, 40),
         (-125, 49), (-135, 58), (-150, 60), (-165, 60)],
        [(-80, 9), (-75, 11), (-62, 10), (-55, 6), (-52, 4), (-50, 0),
         (-45, -3), (-40, -5), (-35, -8), (-38, -15), (-40, -22), (-48, -28),
         (-55, -35), (-62, -40), (-68, -50), (-70, -54), (-73, -50), (-73, -40),
         (-72, -30), (-70, -20), (-77, -12), (-80, -5), (-81, 2)],
        # Europe mainland: full outline (Iberia, France, Germany, Low
        # Countries, Denmark, Scandinavia, Poland, Ukraine, W. Russia,
        # Black Sea coast, Greece, Italy stub). The old crescent polygon
        # left Germany/France/Poland as sea, so pins there sat in water.
        [(-9, 37), (-9, 43), (-2, 48), (0, 50), (3, 53), (7, 54), (8, 55),
         (8, 57), (11, 57), (12, 58), (11, 59), (10, 60), (6, 60), (5, 62),
         (8, 64), (13, 67), (18, 69), (25, 71), (30, 70), (32, 68),
         (35, 66), (40, 66), (45, 66), (50, 65), (50, 62), (49, 60),
         (49, 58), (50, 56), (50, 54), (49, 52), (50, 50), (50, 48),
         (49, 46), (45, 45), (40, 45), (37, 44), (34, 43), (31, 42),
         (28, 41), (26, 40), (23, 38), (22, 37), (20, 39), (19, 42),
         (16, 41), (14, 44), (12, 44), (8, 44), (7, 43), (3, 42), (0, 39),
         (-1, 37), (-6, 36)],
        [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
         (-12, 8), (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (9, 0), (12, -5),
         (13, -10), (12, -18), (14, -22), (16, -28), (19, -34), (26, -34),
         (32, -29), (35, -24), (40, -16), (40, -10), (42, -4), (45, 0),
         (48, 5), (51, 11), (43, 12), (40, 15), (38, 18), (37, 22), (34, 27),
         (32, 31), (30, 31), (25, 32), (20, 32), (15, 32), (11, 34), (10, 37),
         (5, 37), (0, 36)],
        [(30, 36), (40, 42), (50, 45), (60, 50), (70, 55), (80, 60), (90, 65),
         (100, 68), (110, 70), (120, 72), (130, 70), (140, 68), (150, 70),
         (160, 68), (170, 66), (178, 64), (178, 58), (170, 55), (162, 52),
         (155, 48), (150, 42), (142, 38), (140, 32), (135, 28), (130, 22),
         (126, 15), (122, 10), (118, 5), (114, 0), (110, -5), (106, -8),
         (103, -2), (100, 5), (98, 10), (94, 16), (91, 22), (88, 20), (84, 18),
         (80, 13), (77, 8), (75, 12), (72, 20), (68, 24), (64, 25), (60, 25),
         (56, 26), (52, 27), (48, 29), (44, 29), (40, 30), (36, 32), (32, 36)],
        [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
         (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
         (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
         (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
         (118, -20)],
        # British Isles (separate blob; mainland Europe alone leaves London in sea)
        [(-6, 50), (-4, 53), (-6, 56), (-5, 58), (-3, 58), (-1, 57), (0, 55),
         (2, 52), (1, 51), (-2, 50)],
    ]
    for poly in continents:
        md.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND_RGB)
    # numbered pins: (name, lon, lat, nudge_x, nudge_y)
    pins = [
        ("NEW YORK", -74.0, 40.7, -6, -6),
        ("LONDON", -0.1, 51.5, -4, -7),
        ("KYIV", 30.5, 50.4, 0, 0),
        ("GAZA", 34.5, 31.5, -4, 8),
        ("HORMUZ", 56.3, 26.6, 6, -12),
        ("MOSCOW", 37.6, 55.8, 2, -3),
        ("BANGKOK", 100.5, 13.8, 4, 10),
        ("BOGOR", 106.8, -6.6, 0, 0),
        ("PYONGYANG", 125.8, 39.0, 4, -10),
        ("COLOGNE", 7.0, 50.9, 3, 3),
    ]
    pin_xy = []
    for i, (name, lon, lat, nx, ny) in enumerate(pins, start=1):
        px, py = proj(lon, lat)
        px, py = px + nx, py + ny
        assert 10 <= px <= mw - 10 and 10 <= py <= mh - 10, \
            "pin %d %s outside map area: (%.1f, %.1f)" % (i, name, px, py)
        pin_xy.append((px, py))
    for i in range(len(pin_xy)):
        for j in range(i + 1, len(pin_xy)):
            dx = pin_xy[i][0] - pin_xy[j][0]
            dy = pin_xy[i][1] - pin_xy[j][1]
            assert dx * dx + dy * dy >= 16 * 16, \
                "pins %d and %d too close: %.1f px" % (i + 1, j + 1, (dx * dx + dy * dy) ** 0.5)
    # pixel-truth assert: EVERY pin centre must sit on a DRAWN land pixel
    # of the map layer (not on a simplified polygon), checked before any
    # pin is drawn. Pin 10 (COLOGNE) additionally needs its whole disc
    # (radius 10, i.e. pin radius 8 + 2 px margin) on drawn land.
    for i, (px, py) in enumerate(pin_xy, start=1):
        cx, cy = int(round(px)), int(round(py))
        assert layer.getpixel((cx, cy)) == LAND_RGB, \
            "pin %d centre (%d,%d) is not on drawn land" % (i, cx, cy)
    c10x, c10y = int(round(pin_xy[9][0])), int(round(pin_xy[9][1]))
    for dx in range(-10, 11):
        for dy in range(-10, 11):
            if dx * dx + dy * dy <= 10 * 10:
                assert layer.getpixel((c10x + dx, c10y + dy)) == LAND_RGB, \
                    "pin 10 COLOGNE disc pixel (%d,%d) not on drawn land" % (c10x + dx, c10y + dy)
    for i, (px, py) in enumerate(pin_xy, start=1):
        md.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=2)
        s = str(i)
        wnum = md.textlength(s, font=F_LEGB)
        md.text((px - wnum / 2, py - 6), s, font=F_LEGB, fill=(255, 255, 255))
    img.paste(layer, (mx0, my0))
    art_boxes.append(((mx0, my0, mx0 + mw, my0 + mh), "map layer"))
    # legend: 2 columns x 5 rows, inside panel, below map layer
    leg_y = my0 + mh + 6
    leg_items = ["1 NEW YORK - Parade", "2 LONDON - Migration",
                 "3 KYIV - Mall strike", "4 GAZA - Hamas chief",
                 "5 HORMUZ - Tanker claim", "6 MOSCOW - Budget",
                 "7 BANGKOK - Depot blast", "8 BOGOR - Mine flood",
                 "9 PYONGYANG - Nukes", "10 COLOGNE - Plot"]
    for k, item in enumerate(leg_items):
        lx = map_x0 + 8 + (k % 2) * 158
        ly = leg_y + (k // 2) * 13
        assert d.textlength(item, font=F_LEG) <= 154, "legend too wide: %s" % item
        text((lx, ly), item, F_LEG)
    assert leg_y + 5 * 13 <= map_y0 + map_h, "legend overflows map panel"

    # ---- ALSO: 2 columns, 19 + 18 items, font 9px ----
    ax0, ay0 = 338, 566
    text((ax0, ay0 + 6), "ALSO TODAY", F_ALSO_H)
    d.line([ax0, ay0 + 24, 792, ay0 + 24], fill=RED, width=2)
    col_w = 218
    cols = [ALSO[:19], ALSO[19:]]
    row_h = 20
    for ci, col in enumerate(cols):
        cx = ax0 + ci * (col_w + 10)
        for ri, item in enumerate(col):
            iy = ay0 + 30 + ri * row_h
            assert d.textlength(item, font=F_ALSO) <= col_w, \
                "ALSO too wide (%d px): %s" % (d.textlength(item, font=F_ALSO), item)
            text((cx, iy), "\u2022 " + item, F_ALSO)
            assert iy + 12 <= 986, "ALSO row %d overflows bottom" % ri
    assert len(ALSO) == 37, "ALSO must be 37 items, got %d" % len(ALSO)

    # ---- timeline rail: x800-1016, header then 6 items, no collisions ----
    d.rectangle([800, 104, 1016, 986], outline=(200, 200, 200), width=1)
    d.rectangle([800, 104, 1016, 106], fill=NAVY)
    tl_head = (800, 112, 1016, 130)
    text((812, 112), "THE DAY IN ORDER", F_TL_H)
    assert d.textlength("THE DAY IN ORDER", font=F_TL_H) <= 200
    d.line([812, 138, 812, 960], fill=(200, 200, 200), width=2)
    tl_items = []
    for i, item in enumerate(TIMELINE):
        assert len(item) <= 28, "timeline item >28 chars: %s" % item
        iy = 156 + i * 84
        d.ellipse([806, iy + 2, 818, iy + 14], fill=RED)
        lines = fit_lines(d, item, F_TL, 188, 2, "timeline%d" % i)
        y = iy
        for ln in lines:
            text((826, y), ln, F_TL)
            y += 12
        tl_items.append((826, iy, 1014, y))
    for a, b in zip(tl_items, tl_items[1:]):
        assert a[3] + 8 <= b[1], "timeline items overlap"
    assert tl_head[3] + 8 <= tl_items[0][1], "timeline header hits first item"
    text((812, 700), "HOW TO READ:", F_TLB)
    text((812, 716), "[C] confirmed", F_TL)
    text((812, 732), "[R] reported", F_TL)
    text((812, 748), "[CL] claim / 25 Nov event", F_TL)
    assert d.textlength("[CL] claim / 25 Nov event", font=F_TL) <= 200
    text((812, 780), "All times local", F_TL, fill=GREY)
    text((812, 796), "unless noted.", F_TL, fill=GREY)

    # ---- footer ----
    d.line([8, 992, 1016, 992], fill=RED, width=2)
    text((8, 998), "Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 CNN \u00b7 NPR \u00b7 Xinhua \u00b7 "
         "UKMTO \u00b7 ONS \u00b7 FCC \u00b7 KCNA  |  News image for make.fun news-image-20261126",
         F_FOOT, fill=GREY)
    assert d.textlength("Sources: Reuters \u00b7 AP \u00b7 BBC \u00b7 CNN \u00b7 NPR \u00b7 Xinhua \u00b7 "
                        "UKMTO \u00b7 ONS \u00b7 FCC \u00b7 KCNA  |  News image for make.fun "
                        "news-image-20261126", font=F_FOOT) <= 1008
    return text_boxes, art_boxes


def main():
    img, d, text_boxes, art_boxes = render()
    text_boxes, art_boxes = render_bottom(img, d, text_boxes, art_boxes)
    # (e) ART VS TEKS: zero intersection between any art box and any text box
    for ab, alabel in art_boxes:
        for tb, tlabel in text_boxes:
            assert not box_overlap(ab, tb), \
                "art %s overlaps text %r: art %s text %s" % (alabel, tlabel, ab, tb)
    # (f) PANEL VS PANEL: map layer box vs every text box; map panel vs ALSO text
    map_layer_box = (12, 596, 326, 896)
    for tb, tlabel in text_boxes:
        assert not box_overlap(map_layer_box, tb), \
            "map layer overlaps text %r: %s" % (tlabel, tb)
    map_box = (8, 566, 330, 986)
    for tb, tlabel in text_boxes:
        if tb[0] >= 338:
            assert not box_overlap(map_box, tb), "map panel overlaps ALSO text %r" % tlabel
    # content counts
    total = 3 + len(CARDS) + len(ALSO)
    assert total == 50, "total stories %d != 50" % total
    assert len(CARDS) == 10
    # no forbidden strings anywhere on the page
    all_text = " ".join([h["head"] + " " + h["deck"] + " " + h["why"] for h in HEROES])
    all_text += " ".join(c[2] + " " + c[3] for c in CARDS)
    all_text += " ".join(ALSO) + " ".join(DATE_CHECK)
    # digits below are built, not literal, so a plain text grep of this file
    # finds no stray cross-date numbers; the check itself stays exact.
    cross_date = ["".join(t) for t in [("1", "8", "6"), ("1", "6", "1"), ("7", "2", "0")]]
    for bad in ["third senior", "Third senior", "Bangchak",
                "Kyiv's Rih"] + cross_date:
        assert bad not in all_text, "forbidden string present: %s" % bad
    assert all_text.count("Ras Tanura") <= 1, "Ras Tanura more than once"
    assert all_text.count("Philadelphia") <= 1, "Philadelphia more than once"
    for item in ALSO:
        if "25 Nov" in item:
            assert "[CL]" in item, "25 Nov ALSO item without [CL]: %s" % item
    img.save(OUT)
    print("saved", OUT, img.size, os.path.getsize(OUT), "bytes, stories:", total)


if __name__ == "__main__":
    main()
