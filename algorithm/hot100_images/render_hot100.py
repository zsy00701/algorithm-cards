from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "hot100-background.png"
OUT = ROOT / "output"

FONT_REGULAR = str(Path.home() / "Library/Fonts/FandolHei-Regular.otf")
FONT_BOLD = str(Path.home() / "Library/Fonts/FandolHei-Bold.otf")

NAVY = "#0B2E6D"
BLUE = "#1769D2"
LIGHT_BLUE = "#EAF4FF"
MID_BLUE = "#9FC8FF"
GREEN = "#16865A"
GOLD = "#E8A526"
TEXT = "#16233A"
MUTED = "#66758D"
WHITE = "#FFFFFF"


CATEGORIES = [
    ("哈希", [(1, "两数之和"), (49, "字母异位词分组"), (128, "最长连续序列")]),
    ("双指针", [(283, "移动零"), (11, "盛最多水的容器"), (15, "三数之和"), (42, "接雨水")]),
    ("滑动窗口", [(3, "无重复字符的最长子串"), (438, "找到字符串中所有字母异位词")]),
    ("子串", [(560, "和为 K 的子数组"), (239, "滑动窗口最大值"), (76, "最小覆盖子串")]),
    ("普通数组", [(53, "最大子数组和"), (56, "合并区间"), (189, "轮转数组"), (238, "除自身以外数组的乘积"), (41, "缺失的第一个正数")]),
    ("矩阵", [(73, "矩阵置零"), (54, "螺旋矩阵"), (48, "旋转图像"), (240, "搜索二维矩阵 II")]),
    ("链表", [(160, "相交链表"), (206, "反转链表"), (234, "回文链表"), (141, "环形链表"), (142, "环形链表 II"), (21, "合并两个有序链表"), (2, "两数相加"), (19, "删除链表的倒数第 N 个结点"), (24, "两两交换链表中的节点"), (25, "K 个一组翻转链表"), (138, "随机链表的复制"), (148, "排序链表"), (23, "合并 K 个升序链表"), (146, "LRU 缓存")]),
    ("二叉树", [(94, "二叉树的中序遍历"), (104, "二叉树的最大深度"), (226, "翻转二叉树"), (101, "对称二叉树"), (543, "二叉树的直径"), (102, "二叉树的层序遍历"), (108, "将有序数组转换为二叉搜索树"), (98, "验证二叉搜索树"), (230, "二叉搜索树中第 K 小的元素"), (199, "二叉树的右视图"), (114, "二叉树展开为链表"), (105, "从前序与中序遍历序列构造二叉树"), (437, "路径总和 III"), (236, "二叉树的最近公共祖先"), (124, "二叉树中的最大路径和")]),
    ("图论", [(200, "岛屿数量"), (994, "腐烂的橘子"), (207, "课程表"), (208, "实现 Trie（前缀树）")]),
    ("回溯", [(46, "全排列"), (78, "子集"), (17, "电话号码的字母组合"), (39, "组合总和"), (22, "括号生成"), (79, "单词搜索"), (131, "分割回文串"), (51, "N 皇后")]),
    ("二分查找", [(35, "搜索插入位置"), (74, "搜索二维矩阵"), (34, "在排序数组中查找元素的第一个和最后一个位置"), (33, "搜索旋转排序数组"), (153, "寻找旋转排序数组中的最小值"), (4, "寻找两个正序数组的中位数")]),
    ("栈", [(20, "有效的括号"), (155, "最小栈"), (394, "字符串解码"), (739, "每日温度"), (84, "柱状图中最大的矩形")]),
    ("堆", [(215, "数组中的第 K 个最大元素"), (347, "前 K 个高频元素"), (295, "数据流的中位数")]),
    ("贪心", [(121, "买卖股票的最佳时机"), (55, "跳跃游戏"), (45, "跳跃游戏 II"), (763, "划分字母区间")]),
    ("动态规划", [(70, "爬楼梯"), (118, "杨辉三角"), (198, "打家劫舍"), (279, "完全平方数"), (322, "零钱兑换"), (139, "单词拆分"), (300, "最长递增子序列"), (152, "乘积最大子数组"), (416, "分割等和子集"), (32, "最长有效括号")]),
    ("多维动态规划", [(62, "不同路径"), (64, "最小路径和"), (5, "最长回文子串"), (1143, "最长公共子序列"), (72, "编辑距离")]),
    ("技巧", [(136, "只出现一次的数字"), (169, "多数元素"), (75, "颜色分类"), (31, "下一个排列"), (287, "寻找重复数")]),
]

BY_NAME = {name: items for name, items in CATEGORIES}


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def centered(draw, xy, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    x = xy[0] - (box[2] - box[0]) / 2
    y = xy[1] - (box[3] - box[1]) / 2
    draw.text((x, y), text, font=fnt, fill=fill)


def new_canvas():
    return Image.open(BASE).convert("RGBA")


def draw_header(draw, title, subtitle, page):
    centered(draw, (512, 88), title, font(46, True), NAVY)
    draw.rounded_rectangle((190, 137, 834, 184), radius=22, fill=(234, 244, 255, 238), outline=MID_BLUE, width=2)
    centered(draw, (512, 160), subtitle, font(21), TEXT)
    draw.rounded_rectangle((866, 141, 948, 179), radius=18, fill=BLUE)
    centered(draw, (907, 160), page, font(18, True), WHITE)


def fit_text_font(draw, text, max_width, start=24, minimum=17, bold=False):
    for size in range(start, minimum - 1, -1):
        fnt = font(size, bold)
        if draw.textbbox((0, 0), text, font=fnt)[2] <= max_width:
            return fnt
    return font(minimum, bold)


def draw_category_card(draw, x, y, w, name, items, row_h=40):
    header_h = 54
    h = header_h + len(items) * row_h + 22
    draw.rounded_rectangle((x + 4, y + 5, x + w + 4, y + h + 5), radius=18, fill=(11, 46, 109, 25))
    draw.rounded_rectangle((x, y, x + w, y + h), radius=18, fill=(255, 255, 255, 244), outline="#8BB9F1", width=2)
    draw.rounded_rectangle((x, y, x + w, y + header_h), radius=18, fill=LIGHT_BLUE)
    draw.rectangle((x, y + 34, x + w, y + header_h), fill=LIGHT_BLUE)
    draw.rounded_rectangle((x + 16, y + 11, x + 25, y + 43), radius=4, fill=BLUE)
    draw.text((x + 38, y + 10), name, font=font(28, True), fill=NAVY)
    count_text = f"{len(items)} 题"
    count_box = draw.textbbox((0, 0), count_text, font=font(18, True))
    pill_w = count_box[2] + 26
    draw.rounded_rectangle((x + w - pill_w - 16, y + 12, x + w - 16, y + 42), radius=15, fill=BLUE)
    centered(draw, (x + w - pill_w / 2 - 16, y + 27), count_text, font(18, True), WHITE)

    for idx, (number, title) in enumerate(items):
        cy = y + header_h + 11 + idx * row_h
        if idx % 2 == 1:
            draw.rounded_rectangle((x + 12, cy - 2, x + w - 12, cy + row_h - 4), radius=8, fill=(240, 247, 255, 190))
        draw.rounded_rectangle((x + 18, cy + 2, x + 76, cy + 30), radius=13, fill="#DDEEFF")
        centered(draw, (x + 47, cy + 16), str(number), font(17, True), BLUE)
        title_font = fit_text_font(draw, title, w - 132, start=23, minimum=16)
        draw.text((x + 88, cy + 1), title, font=title_font, fill=TEXT)
        draw.ellipse((x + w - 30, cy + 9, x + w - 16, cy + 23), outline="#93BCEB", width=2)
    return h


def draw_footer(draw, text):
    draw.rounded_rectangle((120, 1392, 904, 1444), radius=24, fill=(255, 251, 235, 242), outline="#E9B84B", width=2)
    draw.ellipse((143, 1403, 181, 1441), fill=BLUE)
    centered(draw, (162, 1422), "✓", font(25, True), WHITE)
    centered(draw, (543, 1418), text, font(22, True), NAVY)


def render_detail(filename, title, subtitle, page, left_names, right_names):
    img = new_canvas()
    draw = ImageDraw.Draw(img, "RGBA")
    draw_header(draw, title, subtitle, page)
    columns = [(58, left_names), (522, right_names)]
    total = sum(len(BY_NAME[name]) for name in left_names + right_names)
    for x, names in columns:
        y = 214
        for name in names:
            h = draw_category_card(draw, x, y, 444, name, BY_NAME[name])
            y += h + 20
    draw_footer(draw, f"本页 {total} 题  ·  全套共 100 题")
    img.convert("RGB").save(OUT / filename, quality=96)


def render_overview():
    img = new_canvas()
    draw = ImageDraw.Draw(img, "RGBA")
    draw_header(draw, "力扣 Hot 100 · 分类学习地图", "17 个专题 · 100 道高频题 · 按知识结构分组", "总览")

    positions = []
    x_values = [64, 374, 684]
    y_values = [228, 394, 560, 726, 892, 1058]
    for y in y_values:
        for x in x_values:
            positions.append((x, y))

    accents = [BLUE, "#4056C7", "#0B8E9B", "#11805A", "#7A4CC2", "#C46A1B"]
    for idx, ((name, items), (x, y)) in enumerate(zip(CATEGORIES, positions)):
        w, h = 276, 136
        accent = accents[idx % len(accents)]
        draw.rounded_rectangle((x + 4, y + 5, x + w + 4, y + h + 5), radius=20, fill=(11, 46, 109, 24))
        draw.rounded_rectangle((x, y, x + w, y + h), radius=20, fill=(255, 255, 255, 244), outline="#9CC4F2", width=2)
        draw.rounded_rectangle((x + 16, y + 18, x + 58, y + 60), radius=13, fill=accent)
        centered(draw, (x + 37, y + 39), str(idx + 1), font(21, True), WHITE)
        draw.text((x + 72, y + 18), name, font=fit_text_font(draw, name, 170, 27, 20, True), fill=NAVY)
        draw.text((x + 20, y + 78), f"{len(items)} 道题", font=font(22, True), fill=accent)
        sample = " · ".join(title for _, title in items[:2])
        draw.text((x + 20, y + 108), sample, font=fit_text_font(draw, sample, 236, 16, 12), fill=MUTED)

    draw.rounded_rectangle((64, 1236, 960, 1368), radius=22, fill=(235, 245, 255, 240), outline="#76ACEA", width=2)
    draw.text((88, 1254), "推荐路线", font=font(25, True), fill=NAVY)
    route = "数组字符串 → 链表 → 二叉树 → 搜索回溯 → 栈堆 → 贪心 → 动态规划"
    centered(draw, (512, 1312), route, fit_text_font(draw, route, 820, 25, 18, True), BLUE)
    draw.text((88, 1335), "建议：先掌握模板，再按专题连续刷题，最后进行随机复盘。", font=font(19), fill=TEXT)
    draw_footer(draw, "Hot 100 分类版  ·  题号与题名完整收录")
    img.convert("RGB").save(OUT / "00-hot100-classification-overview.png", quality=96)


def make_contact_sheet():
    files = sorted(OUT.glob("0[0-4]-*.png"))
    thumbs = []
    for file in files:
        image = Image.open(file).convert("RGB")
        image.thumbnail((384, 576), Image.Resampling.LANCZOS)
        thumbs.append(image)
    sheet = Image.new("RGB", (384 * len(thumbs), 576), "white")
    for idx, thumb in enumerate(thumbs):
        sheet.paste(thumb, (idx * 384, 0))
    sheet.save(OUT / "hot100-series-preview.png", quality=94)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assert sum(len(items) for _, items in CATEGORIES) == 100
    render_overview()
    render_detail(
        "01-array-and-string.png",
        "Hot 100 · 数组与字符串",
        "哈希、双指针、滑动窗口、子串、数组、矩阵",
        "1 / 4",
        ["哈希", "双指针", "滑动窗口"],
        ["子串", "普通数组", "矩阵"],
    )
    render_detail(
        "02-linked-list-and-tree.png",
        "Hot 100 · 链表与二叉树",
        "指针操作、递归遍历、树形结构与搜索",
        "2 / 4",
        ["链表"],
        ["二叉树"],
    )
    render_detail(
        "03-search-and-data-structures.png",
        "Hot 100 · 搜索与高级结构",
        "图论、回溯、二分查找、栈、堆",
        "3 / 4",
        ["图论", "回溯"],
        ["二分查找", "栈", "堆"],
    )
    render_detail(
        "04-greedy-and-dp.png",
        "Hot 100 · 贪心与动态规划",
        "局部最优、状态转移、多维 DP 与常用技巧",
        "4 / 4",
        ["贪心", "动态规划"],
        ["多维动态规划", "技巧"],
    )
    make_contact_sheet()


if __name__ == "__main__":
    main()
