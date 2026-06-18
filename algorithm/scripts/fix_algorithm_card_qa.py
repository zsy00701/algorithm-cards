#!/usr/bin/env python3
"""Apply deterministic QA fixes to the six affected algorithm cards."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
CARD_DIR = ROOT / "carl_algorithm_cards" / "gpt-image-2"
FONT_REGULAR = str(Path.home() / "Library/Fonts/FandolHei-Regular.otf")
FONT_BOLD = str(Path.home() / "Library/Fonts/FandolHei-Bold.otf")
FONT_MONO = "/System/Library/Fonts/Menlo.ttc"

BLUE = (13, 75, 190)
GREEN = (18, 118, 59)
LIGHT_GREEN = (246, 252, 247)
WHITE = (255, 255, 255)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def save(image: Image.Image, name: str) -> None:
    if image.size != (1536, 1024):
        raise ValueError(f"unexpected image size for {name}: {image.size}")
    image.save(CARD_DIR / name, format="PNG", optimize=True)


def rounded_result_strip(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    text_size: int,
) -> None:
    draw.rounded_rectangle(box, radius=10, fill=LIGHT_GREEN, outline=(77, 153, 103), width=1)
    x1, y1, x2, y2 = box
    icon_x = x1 + 39
    icon_y = (y1 + y2) // 2
    draw.ellipse((icon_x - 16, icon_y - 16, icon_x + 16, icon_y + 16), fill=(13, 132, 70))
    draw.line((icon_x - 8, icon_y, icon_x - 2, icon_y + 7), fill=WHITE, width=4)
    draw.line((icon_x - 2, icon_y + 7, icon_x + 10, icon_y - 8), fill=WHITE, width=4)

    text_font = font(FONT_BOLD, text_size)
    text_box = draw.textbbox((0, 0), text, font=text_font)
    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]
    available_left = x1 + 78
    available_right = x2 - 16
    text_x = available_left + max(0, (available_right - available_left - text_width) // 2)
    text_y = y1 + (y2 - y1 - text_height) // 2 - text_box[1]
    draw.text((text_x, text_y), text, font=text_font, fill=(20, 35, 28))


def fix_card_15() -> None:
    name = "15-heap-top-k.png"
    image = Image.open(CARD_DIR / name).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle((541, 649, 1108, 681), fill=WHITE)
    save(image, name)


def fix_card_18() -> None:
    name = "18-tree-properties-path.png"
    image = Image.open(CARD_DIR / name).convert("RGB")
    draw = ImageDraw.Draw(image)
    rounded_result_strip(
        draw,
        (36, 665, 1077, 711),
        "结果：示例树平衡（返回高度 3，true）",
        24,
    )
    save(image, name)


def fix_card_20() -> None:
    name = "20-backtracking-combination.png"
    image = Image.open(CARD_DIR / name).convert("RGB")
    draw = ImageDraw.Draw(image)

    # [2] is an unvisited sibling branch, not a pruned branch.
    draw.rectangle((190, 450, 279, 480), fill=WHITE)

    rounded_result_strip(
        draw,
        (40, 641, 1073, 702),
        "结果（组合，按字典序）：[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]",
        22,
    )
    save(image, name)


def fix_card_23() -> None:
    name = "23-backtracking-board.png"
    image = Image.open(CARD_DIR / name).convert("RGB")
    draw = ImageDraw.Draw(image)
    candidate_fill = image.getpixel((365, 445))
    draw.rectangle((360, 441, 404, 476), fill=candidate_fill)
    save(image, name)


def fit_mono(draw: ImageDraw.ImageDraw, text: str, max_width: int) -> ImageFont.FreeTypeFont:
    for size in range(15, 8, -1):
        candidate = font(FONT_MONO, size)
        box = draw.textbbox((0, 0), text, font=candidate)
        if box[2] - box[0] <= max_width:
            return candidate
    raise ValueError("code line cannot fit")


def fix_card_34() -> None:
    name = "34-graph-dfs-bfs-islands.png"
    image = Image.open(CARD_DIR / name).convert("RGB")
    draw = ImageDraw.Draw(image)
    line = "if(i<0||i>=g.size()||j<0||j>=g[0].size()||g[i][j]!='1') return;"
    draw.rectangle((140, 754, 638, 774), fill=WHITE)
    code_font = fit_mono(draw, line, 492)
    draw.text((143, 755), line, font=code_font, fill=(16, 16, 20))
    save(image, name)


def fix_card_36() -> None:
    name = "36-graph-shortest-path.png"
    image = Image.open(CARD_DIR / name).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle((651, 296, 789, 334), fill=WHITE)
    text_font = font(FONT_REGULAR, 15)
    for text, y in (("依次弹出并松弛", 297), ("（D→A→C→B）", 316)):
        box = draw.textbbox((0, 0), text, font=text_font)
        width = box[2] - box[0]
        draw.text((720 - width // 2, y), text, font=text_font, fill=(25, 25, 25))
    save(image, name)


def main() -> None:
    fix_card_15()
    fix_card_18()
    fix_card_20()
    fix_card_23()
    fix_card_34()
    fix_card_36()
    print("fixed: 15, 18, 20, 23, 34, 36")


if __name__ == "__main__":
    main()
