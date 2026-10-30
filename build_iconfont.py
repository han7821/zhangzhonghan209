# -*- coding: utf-8 -*-
"""
build_iconfont.py
=================
从零构建一个 iconfont 风格的图标字体（fontTools 直接绘制轮廓，无外部依赖）。

设计约定（与 iconfont.cn 一致）：
  unitsPerEm = 1024, ascent = 896, descent = -128
  图标在 1024x1024 的网格上绘制（SVG 坐标系，y 轴向下）
  映射: y_font = 896 - y_svg

作者: 张仲涵   课程: 高级网页设计I
"""
import os
import math

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.ttLib import TTFont

UPM = 1024
ASC = 896          # ascent
DESC = -128        # descent
TOP = ASC          # y_svg = 0  ->  y_font = 896

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
CSS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "css")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(CSS_DIR, exist_ok=True)


# ---------------------------------------------------------------- 基础几何
def _flip(p):
    """SVG 坐标(y 向下) -> 字体坐标(y 向上)"""
    return (p[0], TOP - p[1])


def _shoelace(pts):
    s = 0.0
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s


def _contour(start, segs):
    """contour = (start_point, [segment, ...])；segment: ('L', pt) 或 ('C', c1, c2, pt)"""
    return (tuple(start), list(segs))


def _reverse(start, segs):
    """反转闭合轮廓方向"""
    full, cur = [], start
    for s in segs:
        if s[0] == 'L':
            full.append(('L', cur, s[1]))
            cur = s[1]
        else:
            full.append(('C', cur, s[1], s[2], s[3]))
            cur = s[3]
    new = []
    for f in reversed(full):
        if f[0] == 'L':
            new.append(('L', f[1]))
        else:
            new.append(('C', f[3], f[2], f[1]))
    return _contour(start, new)


def poly(pts, cw=True):
    """多边形；cw=True 表示视觉上顺时针（字体中外轮廓方向）"""
    pts = list(pts)
    if (_shoelace(pts) > 0) != cw:
        pts = pts[::-1]
    segs = [('L', tuple(p)) for p in pts[1:]]
    return _contour(pts[0], segs)


def rect(x, y, w, h, cw=True):
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], cw)


K = 0.5522847498307936


def circle(cx, cy, r, cw=True):
    """圆 / 圆环的外圈"""
    p0 = (cx + r, cy)
    p1 = (cx, cy + r)
    p2 = (cx - r, cy)
    p3 = (cx, cy - r)
    segs = [
        ('C', (cx + r, cy + K * r), (cx + K * r, cy + r), p1),
        ('C', (cx - K * r, cy + r), (cx - r, cy + K * r), p2),
        ('C', (cx - r, cy - K * r), (cx - K * r, cy - r), p3),
        ('C', (cx + K * r, cy - r), (cx + r, cy - K * r), p0),
    ]
    c = _contour(p0, segs)
    return c if cw else _reverse(*c)


def ring(cx, cy, r_out, r_in):
    """圆环：外圈顺时针 + 内圈逆时针（非零环绕规则 -> 中间挖空）"""
    return [circle(cx, cy, r_out, True), circle(cx, cy, r_in, False)]


def star(cx, cy, r_out, r_in, n=5):
    pts = []
    for i in range(n * 2):
        ang = math.radians(-90 + i * (180.0 / n))
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return poly(pts, True)


# ---------------------------------------------------------------- 图标绘制
def _draw(contours):
    """contours -> TTGlyphPen glyph（同时做 y 轴翻转 + 三次贝塞尔转二次）"""
    pen = TTGlyphPen(None)
    cpen = Cu2QuPen(pen, max_err=0.6)  # TrueType glyf 只支持二次曲线
    for start, segs in contours:
        cpen.moveTo(_flip(start))
        for s in segs:
            if s[0] == 'L':
                cpen.lineTo(_flip(s[1]))
            else:
                cpen.curveTo(_flip(s[1]), _flip(s[2]), _flip(s[3]))
        cpen.closePath()
    return pen.glyph()


def icon_home():
    return _draw([poly([
        (512, 96), (944, 480), (824, 480), (824, 912),
        (200, 912), (200, 480), (80, 480),
    ])])


def icon_category():
    return _draw([
        rect(96, 96, 288, 288),
        rect(640, 96, 288, 288),
        rect(96, 640, 288, 288),
        rect(640, 640, 288, 288),
    ])


def icon_cart():
    basket = poly([(128, 224), (272, 224), (400, 704), (800, 704), (896, 352), (256, 352)])
    return _draw([basket, circle(416, 800, 72), circle(704, 800, 72)])


def icon_order():
    """订单 / 剪贴板"""
    board = rect(192, 160, 640, 768)          # 外框
    hole = rect(256, 256, 512, 608, cw=False)  # 挖空
    clip = rect(384, 64, 256, 128)             # 顶部夹子
    line1 = rect(320, 368, 384, 64)
    line2 = rect(320, 512, 288, 64)
    line3 = rect(320, 656, 384, 64)
    return _draw([board, hole, clip, line1, line2, line3])


def icon_mine():
    head = circle(512, 320, 160)
    body = _contour((160, 896), [
        ('C', (160, 720), (320, 608), (512, 608)),
        ('C', (704, 608), (864, 720), (864, 896)),
        ('L', (160, 896)),
    ])
    return _draw([head, body])


def icon_search():
    r = ring(432, 432, 272, 176)
    handle = poly([(586, 654), (654, 586), (934, 866), (866, 934)])
    return _draw(r + [handle])


def icon_star():
    return _draw([star(512, 512, 440, 180, 5)])


def icon_heart():
    c = _contour((512, 928), [
        ('C', (384, 800), (128, 640), (128, 448)),
        ('C', (128, 288), (256, 192), (384, 192)),
        ('C', (448, 192), (512, 256), (512, 320)),
        ('C', (512, 256), (576, 192), (640, 192)),
        ('C', (768, 192), (896, 288), (896, 448)),
        ('C', (896, 640), (640, 800), (512, 928)),
    ])
    return _draw([c])


def icon_bell():
    body = _contour((512, 128), [
        ('C', (640, 128), (800, 224), (800, 448)),
        ('L', (800, 640)),
        ('C', (800, 680), (768, 704), (736, 704)),
        ('L', (288, 704)),
        ('C', (256, 704), (224, 680), (224, 640)),
        ('L', (224, 448)),
        ('C', (224, 224), (384, 128), (512, 128)),
    ])
    bar = rect(272, 704, 480, 96)
    clapper = circle(512, 888, 104)
    return _draw([body, bar, clapper])


def icon_plus():
    return _draw([rect(128, 448, 768, 128), rect(448, 128, 128, 768)])


def icon_location():
    pin = _contour((512, 96), [
        ('C', (659, 96), (800, 237), (800, 384)),
        ('C', (800, 592), (512, 928), (512, 928)),
        ('C', (512, 928), (224, 592), (224, 384)),
        ('C', (224, 237), (365, 96), (512, 96)),
    ])
    hole = circle(512, 384, 128, cw=False)
    return _draw([pin, hole])


def icon_arrow_left():
    return _draw([poly([
        (608, 128), (256, 512), (608, 896), (608, 672),
        (928, 672), (928, 352), (608, 352),
    ])])


def icon_arrow_right():
    return _draw([poly([
        (416, 128), (768, 512), (416, 896), (416, 672),
        (96, 672), (96, 352), (416, 352),
    ])])


def icon_more():
    return _draw([circle(192, 512, 84), circle(512, 512, 84), circle(832, 512, 84)])


def icon_scan():
    return _draw([
        rect(96, 96, 240, 64), rect(96, 96, 64, 240),
        rect(688, 96, 240, 64), rect(864, 96, 64, 240),
        rect(96, 864, 240, 64), rect(96, 704, 64, 240),
        rect(688, 864, 240, 64), rect(864, 704, 64, 240),
        rect(160, 480, 704, 64),
    ])


# ---------------------------------------------------------------- 图标清单
# (文件名, 中文名, 码位, 绘制函数)
ICONS = [
    ("home",        "首页",   0xE600, icon_home),
    ("category",    "分类",   0xE601, icon_category),
    ("cart",        "购物车", 0xE602, icon_cart),
    ("order",       "订单",   0xE603, icon_order),
    ("mine",        "我的",   0xE604, icon_mine),
    ("search",      "搜索",   0xE605, icon_search),
    ("star",        "收藏",   0xE606, icon_star),
    ("heart",       "喜欢",   0xE607, icon_heart),
    ("bell",        "消息",   0xE608, icon_bell),
    ("plus",        "加号",   0xE609, icon_plus),
    ("location",    "定位",   0xE60A, icon_location),
    ("arrow-left",  "返回",   0xE60B, icon_arrow_left),
    ("arrow-right", "前进",   0xE60C, icon_arrow_right),
    ("more",        "更多",   0xE60D, icon_more),
    ("scan",        "扫一扫", 0xE60E, icon_scan),
]


def build():
    names = ["icon-" + n for n, _, _, _ in ICONS]
    glyph_order = [".notdef"] + names
    cmap = {cp: "icon-" + n for n, _, cp, _ in ICONS}

    glyphs = {".notdef": TTGlyphPen(None).glyph()}
    for n, _, _, fn in ICONS:
        glyphs["icon-" + n] = fn()

    hmtx = {g: (UPM, 0) for g in glyph_order}

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(hmtx)
    fb.setupHorizontalHeader(ascent=ASC, descent=DESC, lineGap=0)
    fb.setupNameTable({
        "familyName": "iconfont",
        "styleName": "Regular",
        "uniqueFontIdentifier": "iconfont;ZhangZhonghan;AdvancedWebDesignI",
        "fullName": "iconfont",
        "psName": "iconfont",
        "version": "Version 1.0",
    })
    fb.setupOS2(sTypoAscender=ASC, sTypoDescender=DESC, sTypoLineGap=0,
                usWinAscent=ASC, usWinDescent=abs(DESC))
    fb.setupPost()

    ttf_path = os.path.join(OUT_DIR, "iconfont.ttf")
    fb.save(ttf_path)

    for ext, flavor in (("woff", "woff"), ("woff2", "woff2")):
        f = TTFont(ttf_path)
        f.flavor = flavor
        f.save(os.path.join(OUT_DIR, "iconfont." + ext))
        f.close()

    write_css()
    print("OK  ttf/woff/woff2 已生成 ->", OUT_DIR)
    for n, cn, cp, _ in ICONS:
        print("   icon-%-12s U+%04X  %s" % (n, cp, cn))


def write_css():
    """输出与 iconfont.cn 完全一致格式的 CSS（Font class 用法）"""
    lines = []
    lines.append("@font-face {")
    lines.append('  font-family: "iconfont"; /* Project id 4800000 */')
    lines.append("  src: url('../fonts/iconfont.woff2?t=1761580000') format('woff2'),")
    lines.append("       url('../fonts/iconfont.woff?t=1761580000') format('woff'),")
    lines.append("       url('../fonts/iconfont.ttf?t=1761580000') format('truetype');")
    lines.append("}")
    lines.append("")
    lines.append(".iconfont {")
    lines.append('  font-family: "iconfont" !important;')
    lines.append("  font-size: 16px;")
    lines.append("  font-style: normal;")
    lines.append("  -webkit-font-smoothing: antialiased;")
    lines.append("  -moz-osx-font-smoothing: grayscale;")
    lines.append("}")
    lines.append("")
    for n, cn, cp, _ in ICONS:
        lines.append(".icon-%s:before {" % n)
        lines.append('  content: "\\%x";  /* %s */' % (cp, cn))
        lines.append("}")
    lines.append("")

    with open(os.path.join(CSS_DIR, "iconfont.css"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    build()
