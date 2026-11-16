import runpy, os, json, random, zipfile
from PIL import Image

OLD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build_pack.py")
g = runpy.run_path(OLD)
hexc, put, outline, P, ROOT, NAME = g['hexc'], g['put'], g['outline'], g['P'], g['ROOT'], g['NAME']
C = hexc
T = "assets/minecraft/textures/"
CLEAR = (0, 0, 0, 0)


def rect(im, x0, y0, x1, y1, col):
    for y in range(y0, y1):
        for x in range(x0, x1):
            im.putpixel((x, y), col)


def cube(im, u, v, w, h, d, fn):
    faces = {
        'top': (u + d, v, w, d), 'bottom': (u + d + w, v, w, d),
        'left': (u, v + d, d, h), 'front': (u + d, v + d, w, h),
        'right': (u + d + w, v + d, d, h), 'back': (u + 2 * d + w, v + d, w, h),
    }
    for name, (x0, y0, fw, fh) in faces.items():
        for y in range(fh):
            for x in range(fw):
                col = fn(name, x, y, fw, fh)
                if col is not None:
                    im.putpixel((x0 + x, y0 + y), col)


# =============================================================== GUI
DARK, RED, WHITE = C('#1c0f14'), C('#c4232f'), C('#ffffff')
SNOW = C('#e6edf2')
SLOT, SLOT_D, SLOT_L = C('#9db0bb'), C('#5c6f7a'), C('#ffffff')
GOLD = C('#ffcf3f')


def panel(im, w, h):
    rect(im, 0, 0, w, h, DARK)
    for (cx, cy) in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        im.putpixel((cx, cy), CLEAR)
    rect(im, 1, 1, w - 1, h - 1, RED)
    rect(im, 3, 3, w - 3, h - 3, WHITE)
    rect(im, 4, 4, w - 4, h - 4, SNOW)
    # small gold corner studs
    for (cx, cy) in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)):
        im.putpixel((cx, cy), GOLD)


def slot(im, x, y, w=18, h=18):
    rect(im, x, y, x + w, y + h, SLOT)
    for i in range(w):
        im.putpixel((x + i, y), SLOT_D)
        im.putpixel((x + i, y + h - 1), SLOT_L)
    for j in range(h):
        im.putpixel((x, y + j), SLOT_D)
        im.putpixel((x + w - 1, y + j), SLOT_L)
    im.putpixel((x + w - 1, y), SLOT)
    im.putpixel((x, y + h - 1), SLOT)


def arrow(im, x, y, L, hh):
    col = C('#b5c2ca')
    for i in range(L):
        for j in range(hh - 2, hh + 3):
            im.putpixel((x + i, y + j), col)
    for c in range(hh + 1):
        for j in range(c, 2 * hh - c + 1):
            im.putpixel((x + L + c, y + j), col)


def player_slots(im, y_inv, y_hot):
    for r in range(3):
        for c in range(9):
            slot(im, 7 + 18 * c, y_inv + 18 * r)
    for c in range(9):
        slot(im, 7 + 18 * c, y_hot)


def gui_sheet():
    return Image.new("RGBA", (256, 256), CLEAR)


# inventory
inv = gui_sheet()
panel(inv, 176, 166)
for i in range(4):
    slot(inv, 7, 7 + 18 * i)
slot(inv, 76, 61)
x0, y0, x1, y1 = 25, 7, 76, 79
rect(inv, x0, y0, x1, y1, C('#0f3d27'))
for x in range(x0, x1):
    inv.putpixel((x, y0), C('#06140d'))
    inv.putpixel((x, y1 - 1), WHITE)
for y in range(y0, y1):
    inv.putpixel((x0, y), C('#06140d'))
    inv.putpixel((x1 - 1, y), WHITE)
rr = random.Random(2)
for _ in range(14):
    inv.putpixel((rr.randint(x0 + 2, x1 - 3), rr.randint(y0 + 2, y1 - 3)), C('#cfe8f3'))
for (x, y) in ((97, 17), (115, 17), (97, 35), (115, 35)):
    slot(inv, x, y)
slot(inv, 153, 27)
arrow(inv, 136, 31, 9, 5)
player_slots(inv, 83, 141)
inv.save(P(T + "gui/container/inventory.png"))

# crafting table
ct = gui_sheet()
panel(ct, 176, 166)
for r in range(3):
    for c in range(3):
        slot(ct, 29 + 18 * c, 16 + 18 * r)
slot(ct, 119, 30, 26, 26)
arrow(ct, 90, 36, 14, 7)
player_slots(ct, 83, 141)
ct.save(P(T + "gui/container/crafting_table.png"))

# generic_54 (chests, ender chest, barrels)
ch = gui_sheet()
panel(ch, 176, 222)
for r in range(6):
    for c in range(9):
        slot(ch, 7 + 18 * c, 17 + 18 * r)
player_slots(ch, 139, 197)
ch.save(P(T + "gui/container/generic_54.png"))

# shulker box
sb = gui_sheet()
panel(sb, 176, 166)
for r in range(3):
    for c in range(9):
        slot(sb, 7 + 18 * c, 17 + 18 * r)
player_slots(sb, 83, 141)
sb.save(P(T + "gui/container/shulker_box.png"))

# dispenser / dropper
dp = gui_sheet()
panel(dp, 176, 166)
for r in range(3):
    for c in range(3):
        slot(dp, 61 + 18 * c, 16 + 18 * r)
player_slots(dp, 83, 141)
dp.save(P(T + "gui/container/dispenser.png"))

# =============================================================== hotbar
hb = Image.new("RGBA", (182, 22), CLEAR)
rect(hb, 0, 0, 182, 22, (14, 28, 20, 205))
edge = (168, 31, 43, 255)
for x in range(182):
    hb.putpixel((x, 0), edge)
    hb.putpixel((x, 21), edge)
for y in range(22):
    hb.putpixel((0, y), edge)
    hb.putpixel((181, y), edge)
for k in range(8):
    for y in range(1, 21):
        hb.putpixel((20 + 20 * k, y), (90, 105, 98, 255))
hb.save(P(T + "gui/sprites/hud/hotbar.png"))

sel = Image.new("RGBA", (24, 23), CLEAR)
for y in range(23):
    for x in range(24):
        d = min(x, 23 - x, y, 22 - y)
        if d == 0:
            sel.putpixel((x, y), DARK)
        elif d in (1, 2):
            sel.putpixel((x, y), C('#ffd34d'))
sel.save(P(T + "gui/sprites/hud/hotbar_selection.png"))

# =============================================================== hearts
HEART = [".rr.rr.", "rrrrrrr", "rrrrrrr", "rrrrrrr", ".rrrrr.", "..rrr..", "...r..."]
BODY = {(x + 1, y + 1) for y, row in enumerate(HEART) for x, ch_ in enumerate(row) if ch_ == 'r'}


def heart_container(blink):
    im = Image.new("RGBA", (9, 9), CLEAR)
    dil = set()
    for (x, y) in BODY:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                dil.add((x + dx, y + dy))
    oc = C('#ffffff') if blink else C('#0d0709')
    for (x, y) in dil:
        if 0 <= x < 9 and 0 <= y < 9:
            im.putpixel((x, y), oc)
    for p in BODY:
        im.putpixel(p, C('#2b1519'))
    return im


def heart_fill(base, shade, hl, half):
    im = Image.new("RGBA", (9, 9), CLEAR)
    for (x, y) in BODY:
        if half and x > 4:
            continue
        im.putpixel((x, y), shade if (y >= 5 or x >= 6) else base)
    im.putpixel((2, 2), hl)
    im.putpixel((3, 2), hl)
    return im


HS = P(T + "gui/sprites/hud/heart/x.png")[:-5]
heart_container(False).save(HS + "container.png")
heart_container(True).save(HS + "container_blinking.png")
variants = {
    "": (C('#e03348'), C('#a81f2b'), C('#ffe5e8')),
    "_blinking": (C('#ff9aa6'), C('#e86a7a'), C('#ffffff')),
}
absorb = {
    "": (C('#ffcf3f'), C('#c88a14'), C('#fff7d0')),
    "_blinking": (C('#fff0a0'), C('#ffd96a'), C('#ffffff')),
}
for suf, (b, s, h) in variants.items():
    heart_fill(b, s, h, False).save(HS + "full" + suf + ".png")
    heart_fill(b, s, h, True).save(HS + "half" + suf + ".png")
for suf, (b, s, h) in absorb.items():
    heart_fill(b, s, h, False).save(HS + "absorbing_full" + suf + ".png")
    heart_fill(b, s, h, True).save(HS + "absorbing_half" + suf + ".png")

# =============================================================== crafting table blocks
CRED, DCRED = C('#c4232f'), C('#8f1624')
CGRN, DCGRN, LGRN = C('#1f9d55'), C('#0e5c33'), C('#27ad62')
WH = C('#ffffff')

top = Image.new("RGBA", (16, 16))
for y in range(16):
    for x in range(16):
        edge_ = x in (0, 15) or y in (0, 15)
        if edge_:
            c = DCRED
        elif x in (5, 10) or y in (5, 10):
            c = GOLD
        else:
            c = CRED
        top.putpixel((x, y), c)
for a in (2, 7, 12):
    for b in (2, 7, 12):
        top.putpixel((a, b), WH)
top.save(P(T + "block/crafting_table_top.png"))


def wrapped(base, dark, light, ribbon, vertical):
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            if x in (0, 15) or y in (0, 15):
                c = dark
            elif y in (7, 8) or (vertical and x in (7, 8)):
                c = ribbon
            elif (x + y) % 6 == 0:
                c = light
            else:
                c = base
            im.putpixel((x, y), c)
    for (a, b) in ((3, 3), (12, 4), (4, 12), (12, 12)):
        im.putpixel((a, b), WH)
    return im


wrapped(CGRN, DCGRN, LGRN, GOLD, True).save(P(T + "block/crafting_table_front.png"))
wrapped(CRED, DCRED, C('#d83a47'), GOLD, False).save(P(T + "block/crafting_table_side.png"))

# =============================================================== glowstone
gl = Image.new("RGBA", (16, 16))
rg = random.Random(21)
cols = [C('#ffd36b'), C('#ffe08f'), C('#f6bf48'), C('#fff2b0')]
for by in range(0, 16, 2):
    for bx in range(0, 16, 2):
        c = rg.choice(cols)
        rect(gl, bx, by, bx + 2, by + 2, c)
for (a, b) in ((3, 4), (11, 2), (6, 11), (13, 9), (1, 13)):
    gl.putpixel((a, b), WH)
for (a, b) in ((9, 6), (2, 9)):
    gl.putpixel((a, b), CRED)
gl.putpixel((12, 13), CGRN)
gl.save(P(T + "block/glowstone.png"))

# =============================================================== ender chest
GO, DGO = GOLD, C('#c88a14')


def chest_fn(kind):
    def fn(face, x, y, w, h):
        edge_ = x in (0, w - 1) or y in (0, h - 1)
        if face in ('top', 'bottom'):
            if edge_:
                return DCGRN
            if face == 'top' and (x in (w // 2 - 1, w // 2) or y in (h // 2 - 1, h // 2)):
                return CRED
            return LGRN if (x + y) % 5 == 0 else CGRN
        if edge_:
            return DCGRN
        if face in ('front', 'back') and x in (w // 2 - 1, w // 2):
            return CRED
        if kind == 'lid' and y == h - 2:
            return GO
        if kind == 'base' and y == 1:
            return GO
        if (x * 5 + y * 3) % 11 == 0:
            return WH
        return LGRN if (x + y) % 6 == 0 else CGRN
    return fn


ec = Image.new("RGBA", (64, 64), CLEAR)
cube(ec, 0, 0, 14, 5, 14, chest_fn('lid'))
cube(ec, 0, 19, 14, 10, 14, chest_fn('base'))


def latch(face, x, y, w, h):
    if x in (0, w - 1) or y in (0, h - 1):
        return DGO
    return GO


cube(ec, 0, 0, 2, 4, 1, latch)
ec.putpixel((2, 3), CRED)
ec.putpixel((1, 2), CRED)
ec.save(P(T + "entity/chest/ender.png"))

# =============================================================== armor
WHF, WHS = C('#f5f7fa'), C('#cfd8de')
BELT, BOOT = C('#1c0f14'), C('#4d2a11')


def armor(main, shade):
    def s(x, y, w, h):
        return shade if (x == w - 1 or y == h - 1) else main

    def head(face, x, y, w, h):
        if face == 'front':
            if y == 2:
                return WHF
            if y > 2 and 1 <= x <= w - 2:
                return None
            return s(x, y, w, h)
        if face == 'bottom':
            return None
        if face == 'top':
            return WHF if (3 <= x <= 4 and 3 <= y <= 4) else s(x, y, w, h)
        return WHF if y >= 6 else s(x, y, w, h)

    def body(face, x, y, w, h):
        if face == 'top':
            return WHF
        if face == 'bottom':
            return main
        if y in (8, 9):
            if face == 'front' and x in (w // 2 - 1, w // 2):
                return GOLD
            return BELT
        if y >= 10:
            return WHF
        if face == 'front' and x in (w // 2 - 1, w // 2):
            return WHF
        return s(x, y, w, h)

    def arm(face, x, y, w, h):
        if face in ('top', 'bottom'):
            return WHF
        if y >= 10 or y <= 1:
            return WHF
        return s(x, y, w, h)

    def boots(face, x, y, w, h):
        if face == 'top':
            return None
        if face == 'bottom':
            return BOOT
        if y < 7:
            return None
        return WHF if y == 7 else BOOT

    l1 = Image.new("RGBA", (64, 32), CLEAR)
    cube(l1, 0, 0, 8, 8, 8, head)
    cube(l1, 16, 16, 8, 12, 4, body)
    cube(l1, 40, 16, 4, 12, 4, arm)
    cube(l1, 0, 16, 4, 12, 4, boots)

    def body2(face, x, y, w, h):
        if face in ('top', 'bottom') or y < 8:
            return None
        return BELT if y in (8, 9) else main

    def legs2(face, x, y, w, h):
        if face == 'bottom' or y > 6:
            return None
        if y == 0:
            return BELT
        return s(x, y, w, h)

    l2 = Image.new("RGBA", (64, 32), CLEAR)
    cube(l2, 16, 16, 8, 12, 4, body2)
    cube(l2, 0, 16, 4, 12, 4, legs2)
    return l1, l2


sets = {
    'netherite': armor(C('#c4232f'), C('#8f1624')),
    'diamond': armor(C('#1f9d55'), C('#0e5c33')),
}
for mat, (l1, l2) in sets.items():
    l1.save(P(T + f"models/armor/{mat}_layer_1.png"))
    l2.save(P(T + f"models/armor/{mat}_layer_2.png"))
    l1.save(P(T + f"entity/equipment/humanoid/{mat}.png"))
    l2.save(P(T + f"entity/equipment/humanoid_leggings/{mat}.png"))


# =============================================================== FPS: static liquids, light particles
def noise_tex(size, base, var, seed, accents=()):
    im = Image.new("RGBA", (size, size))
    r = random.Random(seed)
    for y in range(size):
        for x in range(size):
            v = r.randint(-var, var)
            im.putpixel((x, y), (min(255, max(0, base[0] + v)), min(255, max(0, base[1] + v)), min(255, max(0, base[2] + v)), 255))
    for (a, b, col) in accents:
        im.putpixel((a % size, b % size), col)
    return im


noise_tex(16, (205, 220, 245), 14, 1, [(3, 4, WH), (11, 9, WH), (7, 13, WH)]).save(P(T + "block/water_still.png"))
noise_tex(32, (205, 220, 245), 14, 2, [(5, 8, WH), (20, 3, WH), (14, 24, WH)]).save(P(T + "block/water_flow.png"))
noise_tex(16, (235, 110, 30), 28, 3, [(4, 5, C('#ffe066')), (11, 10, C('#ffe066')), (8, 2, C('#d62839'))]).save(P(T + "block/lava_still.png"))
noise_tex(32, (235, 110, 30), 28, 4, [(6, 9, C('#ffe066')), (22, 4, C('#ffe066')), (15, 26, C('#d62839'))]).save(P(T + "block/lava_flow.png"))

for i in range(16):
    im = Image.new("RGBA", (16, 16), CLEAR)
    r = 2.0 + i * 0.28
    a = max(0, int(255 * (1 - i / 16)))
    col = (255, 255, 255) if i < 4 else (255, 207, 63) if i < 10 else (214, 40, 57)
    for y in range(16):
        for x in range(16):
            d = ((x + 0.5 - 8) ** 2 + (y + 0.5 - 8) ** 2) ** 0.5
            if d <= r:
                im.putpixel((x, y), col + (a,))
    im.save(P(T + f"particle/explosion_{i}.png"))
for i in range(12):
    Image.new("RGBA", (16, 16), CLEAR).save(P(T + f"particle/big_smoke_{i}.png"))

# =============================================================== metadata + zip
mc = {
    "pack": {
        "pack_format": 34,
        "min_format": 34,
        "max_format": 99,
        "supported_formats": {"min_inclusive": 34, "max_inclusive": 99},
        "description": "§c§lCPVP Pack §r§7by §aJettDashh §8| §f1.21 - 26.1.x\n§7discord: §fhxllxw_x",
    }
}
with open(P("pack.mcmeta"), "w", encoding="utf-8") as f:
    json.dump(mc, f, ensure_ascii=False, indent=2)

zip_path = os.path.join("/home/claude", NAME + ".zip")
if os.path.exists(zip_path):
    os.remove(zip_path)
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for dp_, _, fs in os.walk(ROOT):
        for fn_ in fs:
            full = os.path.join(dp_, fn_)
            z.write(full, os.path.relpath(full, ROOT))

# =============================================================== preview 2
BG = C('#5d6d78')
sheet = Image.new("RGBA", (1120, 1000), BG)


def paste(im, x, y, scale):
    sheet.alpha_composite(im.resize((im.size[0] * scale, im.size[1] * scale), Image.NEAREST), (x, y))


paste(inv.crop((0, 0, 176, 166)), 10, 10, 2)
paste(ct.crop((0, 0, 176, 166)), 372, 10, 2)
ender_gui = Image.new("RGBA", (176, 167), CLEAR)
ender_gui.alpha_composite(ch.crop((0, 0, 176, 71)), (0, 0))
ender_gui.alpha_composite(ch.crop((0, 126, 176, 222)), (0, 71))
paste(ender_gui, 734, 10, 2)
yy = 360
paste(hb, 10, yy, 3)
paste(sel, 10 + 3 * 20 * 2 - 6, yy - 3, 3)
hx = 10
for name in ("container", "full", "half", "full_blinking", "absorbing_full", "container_blinking"):
    paste(Image.open(HS + name + ".png").convert("RGBA"), hx, yy + 90, 6)
    hx += 64
yy = 520
bx = 10
for name in ("crafting_table_top", "crafting_table_front", "crafting_table_side", "glowstone"):
    paste(Image.open(P(T + f"block/{name}.png")).convert("RGBA"), bx, yy, 6)
    bx += 106
paste(ec, 460, yy, 5)
paste(Image.open(P(T + "block/lava_still.png")).convert("RGBA"), 800, yy, 4)
paste(Image.open(P(T + "block/water_still.png")).convert("RGBA"), 880, yy, 4)
yy = 850
ax = 10
for mat, (l1, l2) in sets.items():
    paste(l1, ax, yy, 3)
    paste(l2, ax + 200, yy - 0, 3)
    ax += 420
sheet.convert("RGB").save("cpvp_preview_2.png")
print("done", zip_path)
