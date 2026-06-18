#!/usr/bin/env python3
"""生成两套【原生可编辑】算法方法卡 PPTX：hot100（18）与 carl（36）。

hot100 复用 render_method_cards.py 的源数据；carl 用 carl_cards_data.py（原创撰写）。
原有的图片版 PPT 不受影响，仍保留在 ppt_output/。
"""
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from card_deck_engine import build_deck

OUTDIR = os.path.join(ROOT, "ppt_output")
os.makedirs(OUTDIR, exist_ok=True)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

FOOTER = ""

# --- hot100 ---
rmc = load_module("render_method_cards",
                  os.path.join(ROOT, "hot100_method_cards", "render_method_cards.py"))
hot_spec = {
    "title": "力扣 Hot 100\n算法方法图解",
    "eyebrow": "ALGORITHM MAP",
    "subtitle1": "18 个高频方法专题",
    "subtitle2": "C++ / Python 双语代码模板 · 原生可编辑版",
    "footer": FOOTER,
    "cards": rmc.CARDS,
    "out_path": os.path.join(OUTDIR, "Hot100方法卡_可编辑版.pptx"),
}

# --- carl ---
carl = load_module("carl_cards_data",
                   os.path.join(ROOT, "scripts", "carl_cards_data.py"))
carl_spec = {
    "title": "算法分类\n方法图解（36 讲）",
    "eyebrow": "ALGORITHM MAP",
    "subtitle1": "36 个核心算法专题",
    "subtitle2": "参考代码随想录路线 · C++ / Python 模板 · 原生可编辑版",
    "footer": FOOTER,
    "cards": carl.CARDS,
    "out_path": os.path.join(OUTDIR, "算法分类方法卡36讲_可编辑版.pptx"),
}

for spec in (hot_spec, carl_spec):
    n = build_deck(spec)
    print(f"[完成] {os.path.basename(spec['out_path'])}  {n} 页")
