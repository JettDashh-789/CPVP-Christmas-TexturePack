import os, json, random, zipfile, shutil
from PIL import Image

NAME = "CPVP Pack by JettDashh"
BASE = "/home/claude/cpvp_build"
ROOT = os.path.join(BASE, NAME)
if os.path.exists(BASE):
    shutil.rmtree(BASE)
os.makedirs(ROOT)


def P(path):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    return full


def hexc(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


PAL = {k: hexc(v) for k, v in {
    'r': '#d62839', 'R': '#8f1624', 'w': '#ffffff', 'W': '#cfe8f3',
    'g': '#1f9d55', 'G': '#0e5c33', 'y': '#ffcf3f', 'Y': '#c88a14',
    'b': '#7a4a21', 'B': '#4d2a11', 'i': '#8fd3f4', 'I': '#4aa3d9',
    'L': '#7dfc5b', 'o': '#1c0f14',
}.items()}
OUTLINE = PAL['o']


def new(w=16, h=16):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def from_grid(rows):
    assert len(rows) == 16, len(rows)
    im = new()
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, len(row), row)
        for x, ch in enumerate(row):
            if ch != '.':
                im.putpixel((x, y), PAL[ch])
    return im


def outline(im, col=OUTLINE):
    w, h = im.size
    src = im.copy()
    for y in range(h):
        for x in range(w):
            if src.getpixel((x, y))[3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and src.getpixel((nx, ny))[3] > 0:
                        im.putpixel((x, y), col)
                        break
    return im


def ball(im, cx, cy, rx, ry, light, base, dark):
    for y in range(16):
        for x in range(16):
            dx = (x + 0.5 - cx) / rx
            dy = (y + 0.5 - cy) / ry
            d = dx * dx + dy * dy
            if d <= 1:
                s = (dx + dy) * 0.5
                if s < -0.5:
                    c = light
                elif s > 0.3:
                    c = dark
                else:
                    c = base
                im.putpixel((x, y), c)


def put(im, pts, col):
    for (x, y) in pts:
        if 0 <= x < im.size[0] and 0 <= y < im.size[1]:
            im.putpixel((x, y), col)


# ---------------------------------------------------------------- totem (tree)
tree = [
    "................",
    ".......yy.......",
    "......yyyy......",
    ".......gg.......",
    "......gggg......",
    ".....ggwggg.....",
    "....ggggggrg....",
    "...ggggrgggwg...",
    "..gggwggggrggg..",
    "...ggrggggwgg...",
    "..gggggggwgggr..",
    ".ggggrggggggwgg.",
    ".......bb.......",
    ".......bb.......",
    "......bbbb......",
    "................",
]
# fix row widths that are not 16 (safety) then add shading on the right edge of each green run
fixed = []
for row in tree:
    row = row[:16].ljust(16, '.')
    last = max((i for i, c in enumerate(row) if c != '.'), default=None)
    if last is not None and row[last] == 'g':
        row = row[:last] + 'G' + row[last + 1:]
    fixed.append(row)
totem = outline(from_grid(fixed))
# tiny gold sparkle on the star
totem_img = totem


# ---------------------------------------------------------------- golden apples
def gapple(ribbon, knot, enchanted=False):
    im = new()
    ball(im, 8, 9.4, 5.8, 5.3,
         hexc('#ffe680'), hexc('#ffc72c'), hexc('#c88a14'))
    # ribbon cross
    for y in range(4, 15):
        for x in (7, 8):
            if im.getpixel((x, y))[3] > 0:
                im.putpixel((x, y), ribbon)
    for x in range(2, 14):
        for y in (10,):
            if im.getpixel((x, y))[3] > 0:
                im.putpixel((x, y), ribbon)
    # bow
    put(im, [(5, 2), (6, 2), (5, 3), (6, 3), (9, 2), (10, 2), (9, 3), (10, 3)], ribbon)
    put(im, [(7, 3), (8, 3), (7, 4), (8, 4)], knot)
    put(im, [(5, 6), (4, 7)], PAL['w'])
    if enchanted:
        put(im, [(12, 7), (3, 12), (11, 13)], PAL['w'])
        put(im, [(13, 6), (12, 6), (12, 8)], PAL['i'])
    return outline(im)


gapple_img = gapple(PAL['r'], PAL['R'])
egapple_img = gapple(PAL['g'], PAL['G'], enchanted=True)

# ---------------------------------------------------------------- ender pearl (frosty)
pearl = new()
ball(pearl, 8, 9.8, 5.6, 5.0, hexc('#5fe0bf'), hexc('#1b7f6b'), hexc('#0f4d44'))
put(pearl, [(6, 3), (7, 3), (8, 3), (9, 3)], PAL['y'])
put(pearl, [(7, 1), (8, 1), (6, 2), (9, 2)], PAL['Y'])
put(pearl, [(5, 7), (6, 6), (10, 8), (7, 11), (11, 11), (4, 10)], PAL['w'])
pearl_img = outline(pearl)

# ---------------------------------------------------------------- xp bottle
xp = [
    "................",
    "......rrrr......",
    ".......WW.......",
    "......rrrr......",
    "......WWWW......",
    ".....WLLLLW.....",
    "....WLLLLLLW....",
    "...WLLwLLLLLW...",
    "...WLLLLLLLyW...",
    "...WLLLLLLLLW...",
    "...WLyLLLLLLW...",
    "...WLLLLLLLLW...",
    "....WLLLLLLW....",
    ".....WWWWWW.....",
    "................",
    "................",
]
xp_img = outline(from_grid(xp))

# ---------------------------------------------------------------- crystal item (ornament)
cr = new()
ball(cr, 8, 9.8, 5.6, 5.0, hexc('#ff6b78'), hexc('#d62839'), hexc('#8f1624'))
for y in range(16):
    for x in range(16):
        if cr.getpixel((x, y))[3] > 0 and (x - y) % 6 in (0, 1) and 5 < y < 14:
            cr.putpixel((x, y), PAL['w'])
put(cr, [(6, 3), (7, 3), (8, 3), (9, 3)], PAL['y'])
put(cr, [(7, 1), (8, 1), (6, 2), (9, 2)], PAL['Y'])
crystal_item = outline(cr)


# ---------------------------------------------------------------- candy cane swords
def sword(c1, c2):
    im = new()
    for t in range(0, 9):
        x, y = 14 - t, 2 + t
        col = c1 if (t // 2) % 2 == 0 else c2
        pts = [(x, y)] if t == 0 else [(x, y), (x - 1, y)]
        put(im, pts, col)
    cx, cy = 5, 11
    for k in range(-2, 3):
        put(im, [(cx + k, cy + k), (cx - 1 + k, cy + k)], PAL['y'])
    put(im, [(cx - 2, cy - 2), (cx + 2, cy + 2)], PAL['Y'])
    put(im, [(3, 12)], PAL['b'])
    put(im, [(2, 13)], PAL['B'])
    put(im, [(1, 14), (2, 14)], PAL['y'])
    return outline(im)


netherite_sword = sword(PAL['r'], PAL['w'])
diamond_sword = sword(PAL['g'], PAL['w'])


# ---------------------------------------------------------------- obsidian
def obsidian():
    rnd = random.Random(11)
    im = new()
    for y in range(16):
        for x in range(16):
            v = rnd.randint(-4, 4)
            r, g, b = 0x17 + v, 0x11 + v, 0x27 + v * 2
            if (x + y) % 8 == 0:
                r, g, b = r + 7, g + 6, b + 12
            if y == 0 or x == 0:
                r, g, b = r + 13, g + 12, b + 22
            if y == 15 or x == 15:
                r, g, b = r - 7, g - 6, b - 10
            im.putpixel((x, y), (max(r, 0), max(g, 0), max(b, 0), 255))
    put(im, [(3, 4), (11, 2), (6, 11), (13, 9)], hexc('#cfe8f3'))
    put(im, [(9, 6), (2, 12)], hexc('#d62839'))
    put(im, [(12, 13), (5, 8)], hexc('#1f9d55'))
    return im


obsidian_img = obsidian()


# ---------------------------------------------------------------- end crystal entity texture (64x32)
def face(im, x0, y0, w, h, fn):
    for y in range(h):
        for x in range(w):
            im.putpixel((x0 + x, y0 + y), fn(x, y, w, h))


RED, DRED, WHITE = hexc('#d62839'), hexc('#8f1624'), hexc('#ffffff')


def outer(x, y, w, h):
    if x in (0, w - 1) or y in (0, h - 1):
        return DRED
    return RED if ((x + y) // 2) % 2 == 0 else WHITE


GOLD, DGOLD = hexc('#ffcf3f'), hexc('#c88a14')


def inner(x, y, w, h):
    if x in (0, w - 1) or y in (0, h - 1):
        return DGOLD
    if (x, y) in ((2, 2), (5, 5)):
        return WHITE
    return GOLD


GREEN, DGREEN = hexc('#1f9d55'), hexc('#0e5c33')


def base_top(x, y, w, h):
    if x in (0, w - 1) or y in (0, h - 1):
        return GOLD
    return DGREEN if (x + y) % 2 == 0 else GREEN


def base_side(x, y, w, h):
    if y == 0:
        return GOLD
    if (x * 3 + y) % 7 == 0:
        return WHITE
    return DGREEN if y > 1 else GREEN


crystal = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
for (u, v, fn) in ((0, 0, outer), (32, 0, inner)):
    face(crystal, u + 8, v, 8, 8, fn)        # top
    face(crystal, u + 16, v, 8, 8, fn)       # bottom
    face(crystal, u, v + 8, 8, 8, fn)        # left
    face(crystal, u + 8, v + 8, 8, 8, fn)    # front
    face(crystal, u + 16, v + 8, 8, 8, fn)   # right
    face(crystal, u + 24, v + 8, 8, 8, fn)   # back
face(crystal, 12, 16, 12, 12, base_top)
face(crystal, 24, 16, 12, 12, base_top)
for u in (0, 12, 24, 36):
    face(crystal, u, 28, 12, 4, base_side)


# ---------------------------------------------------------------- low fire (screen overlay)
def fire_strip():
    frames = 32
    strip = Image.new("RGBA", (16, 16 * frames), (0, 0, 0, 0))
    rnd = random.Random(5)
    heights = [3] * 16
    cols = [hexc('#ffe066'), hexc('#ffa733'), hexc('#ff5a1f'), hexc('#d62839')]
    for f in range(frames):
        for x in range(16):
            target = rnd.randint(2, 6)
            heights[x] = round((heights[x] * 2 + target) / 3)
        sm = [heights[max(0, x - 1)] + heights[x] + heights[min(15, x + 1)] for x in range(16)]
        for x in range(16):
            h = max(2, min(6, round(sm[x] / 3)))
            for k in range(h):
                y = 15 - k
                frac = k / max(h - 1, 1)
                c = cols[0] if frac < 0.25 else cols[1] if frac < 0.55 else cols[2] if frac < 0.85 else cols[3]
                if k == h - 1 and h > 3 and rnd.random() < 0.4:
                    continue
                strip.putpixel((x, f * 16 + y), c)
    return strip


# ---------------------------------------------------------------- pack icon
def pack_icon():
    art = Image.new("RGBA", (32, 32))
    for y in range(32):
        t = y / 31
        c = (int(11 + 3 * t), int(61 + 31 * t), int(39 + 12 * t), 255)
        for x in range(32):
            art.putpixel((x, y), c)
    rnd = random.Random(3)
    for _ in range(18):
        art.putpixel((rnd.randint(1, 30), rnd.randint(1, 30)), hexc('#cfe8f3'))
    cx, cy, r = 15.5, 14, 9
    for y in range(32):
        for x in range(32):
            dx, dy = abs(x - cx), abs(y - cy)
            if dx + dy <= r:
                if dx + dy >= r - 1:
                    art.putpixel((x, y), hexc('#ffcf3f'))
                else:
                    art.putpixel((x, y), RED if ((x + y) // 2) % 2 == 0 else WHITE)
    for x in range(32):
        for y in (0, 31):
            art.putpixel((x, y), RED if (x // 2) % 2 == 0 else WHITE)
    for y in range(32):
        for x in (0, 31):
            art.putpixel((x, y), RED if (y // 2) % 2 == 0 else WHITE)
    letters = {
        'C': ["111", "100", "100", "100", "111"],
        'P': ["111", "101", "111", "100", "100"],
        'V': ["101", "101", "101", "101", "010"],
    }
    x0 = 9
    for ch in "CPVP":
        for ry, row in enumerate(letters[ch]):
            for rx, bit in enumerate(row):
                if bit == '1':
                    art.putpixel((x0 + rx, 24 + ry), WHITE)
        x0 += 4
    return art.resize((128, 128), Image.NEAREST)


# ---------------------------------------------------------------- write everything
mc = {
    "pack": {
        "pack_format": 46,
        "min_format": 34,
        "max_format": 99,
        "supported_formats": {"min_inclusive": 34, "max_inclusive": 99},
        "description": "§c§lCPVP Pack §r§7by §aJettDashh\n§7discord: §fhxllxw_x",
    }
}
with open(P("pack.mcmeta"), "w", encoding="utf-8") as f:
    json.dump(mc, f, ensure_ascii=False, indent=2)
with open(P("credits.txt"), "w", encoding="utf-8") as f:
    f.write("CPVP Pack by JettDashh\ndiscord: hxllxw_x\n")

pack_icon().save(P("pack.png"))
base = "assets/minecraft/textures/"
crystal_item.save(P(base + "item/end_crystal.png"))
totem_img.save(P(base + "item/totem_of_undying.png"))
gapple_img.save(P(base + "item/golden_apple.png"))
egapple_img.save(P(base + "item/enchanted_golden_apple.png"))
pearl_img.save(P(base + "item/ender_pearl.png"))
xp_img.save(P(base + "item/experience_bottle.png"))
netherite_sword.save(P(base + "item/netherite_sword.png"))
diamond_sword.save(P(base + "item/diamond_sword.png"))
obsidian_img.save(P(base + "block/obsidian.png"))
crystal.save(P(base + "entity/end_crystal/end_crystal.png"))
fire_strip().save(P(base + "block/fire_1.png"))
with open(P(base + "block/fire_1.png.mcmeta"), "w") as f:
    json.dump({"animation": {"frametime": 2}}, f)

# ---------------------------------------------------------------- zip
zip_path = os.path.join("/home/claude", NAME + ".zip")
if os.path.exists(zip_path):
    os.remove(zip_path)
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for dp, _, fs in os.walk(ROOT):
        for fn in fs:
            full = os.path.join(dp, fn)
            z.write(full, os.path.relpath(full, ROOT))

# ---------------------------------------------------------------- preview sheet
icons = [crystal_item, totem_img, gapple_img, egapple_img, pearl_img, xp_img, netherite_sword, diamond_sword]
S = 6
W = 8 * (16 * S + 10) + 10
sheet = Image.new("RGBA", (W, 16 * S + 20 + 32 * 6 + 20 + 10), hexc('#12171f'))
for i, ic in enumerate(icons):
    sheet.alpha_composite(ic.resize((16 * S, 16 * S), Image.NEAREST), (10 + i * (16 * S + 10), 10))
y2 = 16 * S + 30
sheet.alpha_composite(crystal.resize((64 * 6, 32 * 6), Image.NEAREST), (10, y2))
ob = Image.new("RGBA", (32, 32))
for a in (0, 16):
    for b in (0, 16):
        ob.paste(obsidian_img, (a, b))
sheet.alpha_composite(ob.resize((32 * 6, 32 * 6), Image.NEAREST), (10 + 64 * 6 + 20, y2))
fire = fire_strip().crop((0, 0, 16, 16 * 4))
sheet.alpha_composite(fire.resize((16 * 3, 16 * 4 * 3), Image.NEAREST), (10 + 64 * 6 + 20 + 32 * 6 + 20, y2))
sheet.convert("RGB").save("/home/claude/cpvp_preview.png")
print("ok", zip_path)
