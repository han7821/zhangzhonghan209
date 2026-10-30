# -*- coding: utf-8 -*-
"""build_report.py —— 自动生成《高级网页设计I 图像解决方案 项目报告》.docx"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_COLOR_INDEX
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
OUT = os.path.join(ROOT, "2023xxxxxx-张仲涵-项目报告.docx")

STUDENT_ID = "2023xxxxxx"      # TODO: 替换为真实学号
STUDENT_NAME = "张仲涵"
STUDENT_CLS = "软件工程xx班"    # TODO: 替换为真实班级
TOPIC = "ZZH优选 · 电商商城（移动端下导航 · 图像解决方案）"

doc = Document()

# ---------- 全局默认字体 ----------
normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(10.5)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

sec = doc.sections[0]
sec.top_margin = Cm(2.2)
sec.bottom_margin = Cm(2.0)
sec.left_margin = Cm(2.4)
sec.right_margin = Cm(2.4)


def para(text="", size=10.5, bold=False, align=None, color=None,
         east="宋体", ascii_f="Times New Roman", space_after=4, indent=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
    if align is not None:
        p.alignment = align
    if indent:
        p.paragraph_format.first_line_indent = Pt(21)
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.bold = bold
        r.font.name = ascii_f
        r._element.rPr.rFonts.set(qn("w:eastAsia"), east)
        if color:
            r.font.color.rgb = RGBColor(*color)
    return p


def heading(text, size=12):
    return para(text, size=size, bold=True, east="黑体", ascii_f="Arial",
                space_after=6)


def caption(text):
    return para(text, size=9, align=WD_ALIGN_PARAGRAPH.CENTER,
                color=(0x88, 0x88, 0x88), space_after=8)


def code_block(code, size=8):
    for line in code.rstrip("\n").split("\n"):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:fill"), "F4F4F4")
        pPr.append(shd)
        r = p.add_run(line if line else " ")
        r.font.size = Pt(size)
        r.font.name = "Consolas"
        r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")


def img(path, width=None, height=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(os.path.join(DOCS, path),
                            width=width, height=height)
    return p


def img_cell(cell, path, height):
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(os.path.join(DOCS, path), height=height)


def cap_cell(cell, text):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
    r.font.name = "Times New Roman"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")


# ==================================================== 封面头部
para("《高级网页设计I》", size=18, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, east="黑体", ascii_f="Arial",
     space_after=2)
para("图像解决方案 项目报告", size=15, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, east="黑体", ascii_f="Arial",
     space_after=10)

p = para(space_after=10, align=WD_ALIGN_PARAGRAPH.CENTER)
r = p.add_run("学  号：%s          姓   名：%s" % (STUDENT_ID, STUDENT_NAME))
r.font.size = Pt(11)
r.font.name = "Times New Roman"
r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

t = doc.add_table(rows=1, cols=4)
t.style = "Table Grid"
t.alignment = WD_TABLE_ALIGNMENT.CENTER
cells = t.rows[0].cells
for c, txt in zip(cells, ["班 级", STUDENT_CLS, "项目选题名称", TOPIC]):
    cp = c.paragraphs[0]
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cp.add_run(txt)
    r.font.size = Pt(10)
    r.font.name = "Times New Roman"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
    r.bold = txt in ("班 级", "项目选题名称")
    if "xx" in txt or "xxxxxx" in txt:
        r.font.highlight_color = WD_COLOR_INDEX.YELLOW
para(space_after=6)

# ==================================================== 实施过程
heading("实施过程")

# ---------------- 一 ----------------
heading("一、项目需求与实现")
para("本项目为三级项目“ZZH优选 · 电商商城”提供图像解决方案：采用 iconfont 的 "
     "Font class（字体图标）方案，为移动端电商页面提供下导航（TabBar）及页面内全部图标。"
     "页面包含首页、分类、购物车、订单、我的 5 个下导航页面；下导航固定于视口底部，"
     "选中项图标与文字高亮（#ff5000），购物车 Tab 带红色未读徽标；"
     "同时适配 320~768 等多种视口，并在 Edge、Chrome 双浏览器下完成测试。", indent=True)

para("1. 从 iconfont 获得的所有图标的截图", bold=True, space_after=2)
img("shot_iconlib.png", width=Cm(14.5))
caption("图 1  iconfont 字体图标库（15 个图标，U+E600~U+E60E，生成 iconfont.woff2 / woff / ttf 三种格式）")

para("2. 下导航原图", bold=True, space_after=2)
img("shot_wireframe.png", width=Cm(9.5))
caption("图 2  下导航设计原图（低保真线框图，375×667 设计稿，含设计规格说明）")

para("3. 下导航实现图", bold=True, space_after=2)
t = doc.add_table(rows=2, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
img_cell(t.rows[0].cells[0], "shot_home_375.png", Cm(10.5))
img_cell(t.rows[0].cells[1], "shot_cart_375.png", Cm(10.5))
cap_cell(t.rows[0].cells[0], "图 3  首页（下导航实现图，选中“首页”）")
cap_cell(t.rows[0].cells[1], "图 4  购物车页（选中“购物车”，带徽标）")
img_cell(t.rows[1].cells[0], "shot_order_375.png", Cm(10.5))
img_cell(t.rows[1].cells[1], "shot_mine_375.png", Cm(10.5))
cap_cell(t.rows[1].cells[0], "图 5  订单页（选中“订单”）")
cap_cell(t.rows[1].cells[1], "图 6  我的页（选中“我的”）")

# ---------------- 二 ----------------
heading("二、项目代码")
para("图标方案：iconfont Font class。@font-face 依次声明 woff2 / woff / ttf 三种格式，"
     "浏览器按兼容性自动选择；.iconfont 为基础类，每个图标以 .icon-xxx:before 的 "
     "content 码位（U+E600~U+E60E）呈现，页面中用 <i class=\"iconfont icon-home\"></i> 引用。"
     "CSS 设计：全局样式表 global.css 中完成 Reset、:root CSS 变量、公共工具类；"
     "业务类名统一使用姓名缩写前缀 zzh-，未使用 id 选择器；"
     "代码中（HTML 注释、meta、JS 常量与页面页脚）均包含学号与姓名。", indent=True)

para("核心代码 1：HTML 头部与下导航结构（index.html 节选）", bold=True, space_after=2)
code_block("""
<!-- 高级网页设计I 三级项目：ZZH优选 电商商城
     学号：2023xxxxxx   姓名：张仲涵
     图标方案：iconfont Font class（字体图标） -->
<meta name="author" content="张仲涵 2023xxxxxx">
<link rel="stylesheet" href="css/global.css">
<link rel="stylesheet" href="css/iconfont.css">

<!-- 下导航：iconfont 字体图标 -->
<nav class="zzh-nav" id="zzhNav">
  <a class="zzh-nav__item zzh-nav__item--active" href="javascript:;" data-page="home">
    <i class="iconfont icon-home"></i><span>首页</span>
  </a>
  <a class="zzh-nav__item" href="javascript:;" data-page="category">
    <i class="iconfont icon-category"></i><span>分类</span>
  </a>
  <a class="zzh-nav__item" href="javascript:;" data-page="cart">
    <i class="iconfont icon-cart"></i><span>购物车</span>
    <em class="zzh-nav__badge">2</em>
  </a>
  <a class="zzh-nav__item" href="javascript:;" data-page="order">
    <i class="iconfont icon-order"></i><span>订单</span>
  </a>
  <a class="zzh-nav__item" href="javascript:;" data-page="mine">
    <i class="iconfont icon-mine"></i><span>我的</span>
  </a>
</nav>
""")

para("核心代码 2：iconfont.css 的 @font-face 与基础类（节选）", bold=True, space_after=2)
code_block("""
@font-face {
  font-family: "iconfont";
  src: url('../fonts/iconfont.woff2?t=1761580000') format('woff2'),
       url('../fonts/iconfont.woff?t=1761580000') format('woff'),
       url('../fonts/iconfont.ttf?t=1761580000') format('truetype');
}
.iconfont {
  font-family: "iconfont" !important;
  font-size: 16px; font-style: normal;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.icon-home:before     { content: "\\e600"; }  /* 首页   */
.icon-category:before { content: "\\e601"; }  /* 分类   */
.icon-cart:before     { content: "\\e602"; }  /* 购物车 */
.icon-order:before    { content: "\\e603"; }  /* 订单   */
.icon-mine:before     { content: "\\e604"; }  /* 我的   */
""")

para("核心代码 3：下导航全局样式（css/global.css 节选，含 CSS 变量）", bold=True, space_after=2)
code_block("""
:root {
  --zzh-primary: #ff5000;   /* 主色：电商橙 */
  --zzh-nav-h:   54px;      /* 下导航高度 */
  --zzh-line:    #ededed;
  --zzh-radius:  10px;
}
/* 下导航：fixed 底部定位 + 安全区适配 + 限宽居中 */
.zzh-nav {
  position: fixed; bottom: 0; left: 50%; transform: translateX(-50%);
  width: 100%; max-width: 480px;
  height: var(--zzh-nav-h);
  background: #fff;
  border-top: 1px solid var(--zzh-line);
  display: flex;
  z-index: 30;
  padding-bottom: env(safe-area-inset-bottom);
}
.zzh-nav__item {
  flex: 1;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 3px;
  color: var(--zzh-text-2); font-size: 11px;
  transition: color .2s;
}
.zzh-nav__item .iconfont { font-size: 23px; line-height: 1; }
.zzh-nav__item--active { color: var(--zzh-primary); font-weight: 600; }
.zzh-nav__badge {
  position: absolute; top: 4px; left: 58%;
  min-width: 16px; height: 16px; line-height: 16px;
  background: #ff4d4f; color: #fff;
  border-radius: 8px; font-size: 10px; padding: 0 4px;
}
""")

para("核心代码 4：下导航页面切换（js/main.js 节选，代码中包含学号姓名）", bold=True, space_after=2)
code_block("""
// 学生信息（课程要求：代码中需包含学号或姓名）
var STUDENT = { id: '2023xxxxxx', name: '张仲涵', cls: '软件工程xx班' };

var navItems = document.querySelectorAll('#zzhNav .zzh-nav__item');
var pages = document.querySelectorAll('.zzh-page');

function activate(name) {
  navItems.forEach(function (n) {
    n.classList.toggle('zzh-nav__item--active',
                       n.getAttribute('data-page') === name);
  });
  pages.forEach(function (p) { p.classList.remove('zzh-page--active'); });
  var page = document.getElementById('page-' + name);
  if (page) { page.classList.add('zzh-page--active'); window.scrollTo(0, 0); }
}

navItems.forEach(function (item) {
  item.addEventListener('click', function () {
    var target = item.getAttribute('data-page');
    location.hash = target;      // 支持地址栏直达，如 index.html#cart
    activate(target);
  });
});
""")

# ---------------- 三 ----------------
heading("三、测试与发布")
para("测试环境：Windows 11；浏览器 Microsoft Edge 141 与 Google Chrome 141；"
     "测试视口：320×568（小屏）、375×812（iPhone X 基准）、414×896（大屏）、"
     "768×1024（平板）。采用 Chrome DevTools 协议（puppeteer-core）进行设备模拟自动化截图，"
     "全部截图均为 2 倍像素密度（Retina）。", indent=True)

para("1. 不同视口下的测试截图", bold=True, space_after=2)
t = doc.add_table(rows=2, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
img_cell(t.rows[0].cells[0], "shot_home_320.png", Cm(10.2))
img_cell(t.rows[0].cells[1], "shot_home_375.png", Cm(10.2))
cap_cell(t.rows[0].cells[0], "图 7  320×568 小屏视口（Edge）")
cap_cell(t.rows[0].cells[1], "图 8  375×812 基准视口（Edge）")
img_cell(t.rows[1].cells[0], "shot_home_414.png", Cm(10.2))
img_cell(t.rows[1].cells[1], "shot_home_768.png", Cm(10.2))
cap_cell(t.rows[1].cells[0], "图 9  414×896 大屏视口（Edge）")
cap_cell(t.rows[1].cells[1], "图 10  768×1024 平板视口（限宽 480px 居中，Edge）")

para("2. 不同浏览器下的测试截图（真实浏览器窗口，地址栏可见）", bold=True, space_after=2)
t = doc.add_table(rows=1, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
img_cell(t.rows[0].cells[0], "shot_browser_home_edge.png", Cm(10.2))
img_cell(t.rows[0].cells[1], "shot_browser_home_chrome.png", Cm(10.2))
cap_cell(t.rows[0].cells[0], "图 11  Microsoft Edge 浏览器")
cap_cell(t.rows[0].cells[1], "图 12  Google Chrome 浏览器")

para("3. 发布截图", bold=True, space_after=2)
para("项目通过本地 HTTP 服务器（自建服务器方式）发布：在项目根目录执行"
     "“python -m http.server 8765”，将 zzh-shop 目录作为站点根目录对外提供访问，"
     "浏览器访问 http://127.0.0.1:8765/index.html 即可查看，"
     "图 11、图 12 地址栏中可见发布后的访问地址，页面字体图标、下导航交互均正常。", indent=True)

# ---------------- 项目总结 ----------------
heading("项目总结")
para("本次项目我完整地实践了一套 Web 图像解决方案：从图标资源整理、字体文件生成、"
     "CSS 封装，到页面实现与多环境测试。收获主要有三点："
     "一是真正理解了字体图标（@font-face + :before content 码位）的原理——"
     "图标本质是字体字形，因此可以像文字一样用 color、font-size 无损缩放与换色，"
     "相比雪碧图省去了定位换算，相比 SVG symbol 又保持了单文件、零请求的成本优势；"
     "二是掌握了移动端下导航的实现要点：position: fixed + left:50% + translateX(-50%) "
     "配 max-width 限宽，使导航在手机全屏与平板居中两种场景下都表现正确，"
     "并用 env(safe-area-inset-bottom) 适配全面屏安全区；"
     "三是建立了全局 CSS 的组织方式：Reset、:root 变量、工具类分层，"
     "业务类名统一加姓名缩写前缀 zzh-，避免命名冲突，也满足课程对代码规范的要求。", indent=True)
para("教训方面：字体图标初次引入时出现基线偏移，通过给 .iconfont 设置 line-height:1 "
     "并统一字号解决；fixed 底栏在小屏上曾被软键盘与长内容遮挡，改为容器 padding-bottom "
     "预留导航高度后修复；截图测试时发现 Windows 下无头浏览器视口有约 500px 的最小宽度限制，"
     "无法直接模拟 375px 手机视口，最终改用 DevTools 协议的设备模拟完成。", indent=True)
para("AI 使用说明：本项目使用了 WorkBuddy AI 助手辅助完成，具体方法为："
     "（1）让 AI 依据 iconfont 规范（unitsPerEm=1024、ascent=896）编写 Python + fontTools "
     "脚本，批量绘制 15 个图标的轮廓并生成 iconfont.ttf / woff / woff2 字体文件与 "
     "iconfont.css；（2）由 AI 生成页面 HTML / CSS / JS 初稿，再人工审查并调整视觉细节；"
     "（3）用 AI 编写基于 puppeteer-core 的自动化截图脚本，完成多视口、双浏览器的测试取证；"
     "（4）用 python-docx 自动排版生成本报告并插入截图。"
     "AI 主要承担了重复性、工具性的工作，页面结构设计、样式取舍与测试结论由本人确认，"
     "全部代码均经本地运行与双浏览器实测验证。", indent=True)
para("项目报告提交文件名：%s-%s（学号-姓名）。" % (STUDENT_ID, STUDENT_NAME), indent=True)

doc.save(OUT)
print("OK ->", OUT)
