#!/usr/bin/env python3
"""生成 README 顶部 hero 横幅：导航蓝标题带 + 4 张精选卡缩略。"""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]          # algorithm/
OUT = ROOT / "assets" / "hero.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

ZH_BOLD = str(Path.home() / "Library/Fonts/FandolHei-Bold.otf")
ZH_REG = str(Path.home() / "Library/Fonts/FandolHei-Regular.otf")

NAVY = (11, 46, 109)
CYAN = (139, 194, 255)
WHITE = (255, 255, 255)
PALE = (244, 249, 255)
BORDER = (21, 89, 199)

CARDS = [
    ROOT / "hot100_method_cards/gpt-image-2/01-hash-gpt-image-2.png",
    ROOT / "hot100_method_cards/gpt-image-2/13-monotonic-stack-gpt-image-2.png",
    ROOT / "carl_algorithm_cards/gpt-image-2/01-array-binary-search.png",
    ROOT / "carl_algorithm_cards/gpt-image-2/34-graph-dfs-bfs-islands.png",
]

W = 1600
BAND = 168           # 标题带高度
PAD = 40
GAP = 24
N = len(CARDS)
card_w = (W - 2 * PAD - (N - 1) * GAP) // N
card_h = round(card_w / 1.5)            # 卡片 3:2
H = BAND + 28 + card_h + PAD

img = Image.new("RGB", (W, H), PALE)
d = ImageDraw.Draw(img)

# 标题带
d.rectangle((0, 0, W, BAND), fill=NAVY)
d.rectangle((0, BAND, W, BAND + 6), fill=CYAN)
d.rectangle((PAD, 40, PAD + 90, 50), fill=CYAN)
title = ImageFont.truetype(ZH_BOLD, 58)
sub = ImageFont.truetype(ZH_REG, 27)
en = ImageFont.truetype(ZH_REG, 22)
d.text((PAD, 62), "算法方法图解卡", font=title, fill=WHITE)
d.text((PAD, 130), "LeetCode Hot 100 + 代码随想录路线 · 一题型一张 · C++ / Python 模板",
       font=sub, fill=CYAN)

# 右上角统计
stat = ImageFont.truetype(ZH_BOLD, 40)
statlbl = ImageFont.truetype(ZH_REG, 22)
box = d.textbbox((0, 0), "54", font=stat)
d.text((W - PAD - 250, 56), "54", font=stat, fill=WHITE)
d.text((W - PAD - 250, 104), "张方法卡", font=statlbl, fill=CYAN)
d.text((W - PAD - 110, 56), "2", font=stat, fill=WHITE)
d.text((W - PAD - 110, 104), "套题集", font=statlbl, fill=CYAN)

# 卡片缩略
y = BAND + 28
for i, p in enumerate(CARDS):
    x = PAD + i * (card_w + GAP)
    c = Image.open(p).convert("RGB").resize((card_w, card_h), Image.Resampling.LANCZOS)
    img.paste(c, (x, y))
    d.rectangle((x, y, x + card_w - 1, y + card_h - 1), outline=BORDER, width=3)

img.save(OUT, quality=92)
print(f"[完成] {OUT}  ({W}x{H})")
