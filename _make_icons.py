# 生成 PWA 图标：深蓝底 + 人形/齿轮意象（三个头像 + 进度条），纯 PIL 绘制
from PIL import Image, ImageDraw
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
os.makedirs(OUT, exist_ok=True)

BG = (31, 42, 68)      # #1f2a44
BLUE = (79, 143, 247)  # #4f8ff7
GREEN = (40, 167, 106)
AMBER = (214, 148, 60)
WHITE = (255, 255, 255)


def draw(size, maskable=False):
    img = Image.new("RGBA", (size, size), BG + (255,))
    d = ImageDraw.Draw(img)
    s = size / 512.0
    # 顶部高光条（模拟导航栏）
    if not maskable:
        d.rectangle([0, 0, size, int(46 * s)], fill=(23, 31, 50, 255))
    # 三个头像：通讯录意象
    def avatar(cx, cy, r, color):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    def body(cx, cy, r, color):
        # 半身：圆头 + 肩
        hr = r
        d.ellipse([cx - hr, cy - hr * 1.35, cx + hr, cy + hr * 0.65], fill=color)
        d.pieslice([cx - r * 1.25, cy + hr * 0.15, cx + r * 1.25, cy + hr * 0.15 + r * 2.2], 180, 360, fill=color)

    body(150 * s, 210 * s, 52 * s, WHITE)
    body(256 * s, 180 * s, 62 * s, BLUE)
    body(362 * s, 210 * s, 52 * s, (150, 168, 196, 255))
    # 底部三条进度条：排产/效率
    bars = [(0.92, GREEN), (0.68, BLUE), (0.44, AMBER)]
    y = 352 * s
    for i, (pct, color) in enumerate(bars):
        yy = y + i * 52 * s
        d.rounded_rectangle([80 * s, yy, 432 * s, yy + 26 * s], radius=13 * s, fill=(255, 255, 255, 40))
        d.rounded_rectangle([80 * s, yy, 80 * s + 352 * s * pct, yy + 26 * s], radius=13 * s, fill=color)

    # maskable 需要安全区：图形缩到中心 80%
    if maskable:
        pass
    return img


for size, name, mk in [(192, "icon-192.png", False), (512, "icon-512.png", False),
                       (512, "icon-maskable-512.png", True), (180, "apple-touch-icon.png", False)]:
    im = draw(size, mk)
    if mk:
        # maskable：留 20% 边距，重绘缩放
        canvas = Image.new("RGBA", (512, 512), BG + (255,))
        im = im.resize((410, 410), Image.LANCZOS)
        canvas.paste(im, (51, 51), im)
        im = canvas
    im.save(os.path.join(OUT, name), "PNG", optimize=True)
    print("wrote", name, im.size)
