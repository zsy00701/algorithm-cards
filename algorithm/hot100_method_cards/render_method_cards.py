from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "method-card-background.png"
OUT = ROOT / "output"

ZH_REG = str(Path.home() / "Library/Fonts/FandolHei-Regular.otf")
ZH_BOLD = str(Path.home() / "Library/Fonts/FandolHei-Bold.otf")
MONO = "/System/Library/Fonts/Menlo.ttc"

NAVY = "#0B2E6D"
BLUE = "#1769D2"
CYAN = "#2D95E8"
PALE = "#E8F3FF"
PALE2 = "#F4F9FF"
GOLD = "#E9A51D"
GREEN = "#15845B"
RED = "#D94C4C"
TEXT = "#17243A"
MUTED = "#607087"
WHITE = "#FFFFFF"


CARDS = [
    {
        "slug": "01-hash",
        "title": "哈希表（Hash Map / Set）",
        "definition": "用“键 → 信息”的映射保存已见元素，把查找从 O(n) 降为平均 O(1)。",
        "signals": ["配对 / 去重 / 计数", "快速判断是否出现", "空间换时间"],
        "steps": ["确定 key 与要保存的信息", "遍历时先查询当前所需 key", "命中则更新答案或返回", "未命中则写入哈希表"],
        "example": "两数之和：nums = [2, 7, 11, 15]，target = 9",
        "visual": "hash",
        "hot": "Hot 100：1 两数之和｜49 字母异位词分组｜128 最长连续序列",
        "memory": "记忆：需要“秒查”某个值，就先想到哈希表",
        "cpp": """vector<int> twoSum(vector<int>& a, int target) {
    unordered_map<int,int> pos;
    for (int i = 0; i < a.size(); ++i) {
        int need = target - a[i];
        if (pos.count(need)) return {pos[need], i};
        pos[a[i]] = i;
    }
    return {};
}""",
        "py": """def two_sum(a, target):
    pos = {}
    for i, x in enumerate(a):
        need = target - x
        if need in pos:
            return [pos[need], i]
        pos[x] = i
    return []""",
    },
    {
        "slug": "02-two-pointers",
        "title": "双指针（Two Pointers）",
        "definition": "用两个位置协同扫描，利用单调性跳过无效状态，常把 O(n²) 降到 O(n)。",
        "signals": ["有序数组 / 链表", "首尾夹逼或快慢同行", "寻找配对、区间或原地修改"],
        "steps": ["根据问题放置左右指针", "计算当前状态并更新答案", "移动更可能改善答案的一侧", "直到指针相遇或越界"],
        "example": "盛最多水的容器：短板决定面积，移动短板一侧",
        "visual": "two_pointers",
        "hot": "Hot 100：283 移动零｜11 盛最多水的容器｜15 三数之和｜42 接雨水",
        "memory": "记忆：有序 + 两端决策 → 相向双指针",
        "cpp": """int maxArea(vector<int>& h) {
    int l = 0, r = h.size() - 1, ans = 0;
    while (l < r) {
        ans = max(ans, min(h[l], h[r]) * (r-l));
        if (h[l] < h[r]) ++l;
        else --r;
    }
    return ans;
}""",
        "py": """def max_area(h):
    l, r, ans = 0, len(h) - 1, 0
    while l < r:
        ans = max(ans, min(h[l], h[r]) * (r-l))
        if h[l] < h[r]: l += 1
        else: r -= 1
    return ans""",
    },
    {
        "slug": "03-sliding-window",
        "title": "滑动窗口（Sliding Window）",
        "definition": "维护一个连续区间及其状态，让左右边界只向前移动，在线性时间处理子数组/子串。",
        "signals": ["连续子数组 / 子串", "最长、最短、满足条件", "窗口状态可增量维护"],
        "steps": ["右指针扩张并加入新元素", "窗口不合法时移动左指针", "同步删除左侧元素状态", "每轮更新最长或最短答案"],
        "example": "无重复字符的最长子串：窗口内字符必须唯一",
        "visual": "window",
        "hot": "Hot 100：3 无重复字符的最长子串｜438 找到字符串中所有字母异位词｜76 最小覆盖子串",
        "memory": "记忆：右扩张、左收缩，窗口始终保持合法",
        "cpp": """int lengthOfLongestSubstring(string s) {
    unordered_set<char> win;
    int l = 0, ans = 0;
    for (int r = 0; r < s.size(); ++r) {
        while (win.count(s[r])) win.erase(s[l++]);
        win.insert(s[r]);
        ans = max(ans, r - l + 1);
    }
    return ans;
}""",
        "py": """def length_of_longest_substring(s):
    win, l, ans = set(), 0, 0
    for r, ch in enumerate(s):
        while ch in win:
            win.remove(s[l]); l += 1
        win.add(ch)
        ans = max(ans, r - l + 1)
    return ans""",
    },
    {
        "slug": "04-prefix-sum",
        "title": "前缀和 + 哈希",
        "definition": "把区间和转成两个前缀和之差；再用哈希统计历史前缀和出现次数。",
        "signals": ["连续区间和", "区间和等于 K", "需要统计区间数量"],
        "steps": ["初始化 count[0] = 1", "累加当前前缀和 pre", "答案增加 count[pre-K]", "再记录 count[pre]++"],
        "example": "和为 K 的子数组：[1, 1, 1]，K = 2，共 2 个",
        "visual": "prefix",
        "hot": "Hot 100：560 和为 K 的子数组｜238 除自身以外数组的乘积（前后缀思想）",
        "memory": "记忆：区间和 = pre[r] - pre[l-1]",
        "cpp": """int subarraySum(vector<int>& a, int k) {
    unordered_map<int,int> cnt{{0,1}};
    int pre = 0, ans = 0;
    for (int x : a) {
        pre += x;
        ans += cnt[pre - k];
        ++cnt[pre];
    }
    return ans;
}""",
        "py": """def subarray_sum(a, k):
    cnt, pre, ans = {0: 1}, 0, 0
    for x in a:
        pre += x
        ans += cnt.get(pre - k, 0)
        cnt[pre] = cnt.get(pre, 0) + 1
    return ans""",
    },
    {
        "slug": "05-sort-intervals",
        "title": "排序 + 区间合并",
        "definition": "先排序建立单调顺序，再扫描合并重叠区间，避免重复比较。",
        "signals": ["区间重叠 / 覆盖", "顺序混乱但可排序", "合并、删除或选择区间"],
        "steps": ["按区间左端点排序", "维护结果中的最后区间", "若重叠，扩展右端点", "否则加入一个新区间"],
        "example": "合并区间：[1,3] [2,6] [8,10] → [1,6] [8,10]",
        "visual": "intervals",
        "hot": "Hot 100：56 合并区间｜53 最大子数组和｜189 轮转数组｜41 缺失的第一个正数",
        "memory": "记忆：区间题先排序，再只盯住“最后一个区间”",
        "cpp": """vector<vector<int>> merge(vector<vector<int>>& a) {
    sort(a.begin(), a.end());
    vector<vector<int>> ans;
    for (auto& p : a) {
        if (ans.empty() || ans.back()[1] < p[0])
            ans.push_back(p);
        else ans.back()[1] = max(ans.back()[1], p[1]);
    }
    return ans;
}""",
        "py": """def merge(intervals):
    ans = []
    for l, r in sorted(intervals):
        if not ans or ans[-1][1] < l:
            ans.append([l, r])
        else:
            ans[-1][1] = max(ans[-1][1], r)
    return ans""",
    },
    {
        "slug": "06-matrix-simulation",
        "title": "矩阵模拟（边界 / 方向）",
        "definition": "把二维操作拆成方向变化或四条边界收缩，重点处理边界与访问顺序。",
        "signals": ["旋转、螺旋、置零", "二维坐标变换", "按层或按方向遍历"],
        "steps": ["定义上、下、左、右边界", "按固定方向遍历一条边", "完成后收缩对应边界", "每次转向前检查边界"],
        "example": "螺旋矩阵：右 → 下 → 左 → 上，逐层收缩",
        "visual": "matrix",
        "hot": "Hot 100：73 矩阵置零｜54 螺旋矩阵｜48 旋转图像｜240 搜索二维矩阵 II",
        "memory": "记忆：方向固定，边界收缩；转向之前先判越界",
        "cpp": """vector<int> spiralOrder(vector<vector<int>>& a) {
    vector<int> ans; int t=0,b=a.size()-1,l=0,r=a[0].size()-1;
    while (t <= b && l <= r) {
        for (int j=l;j<=r;++j) ans.push_back(a[t][j]); ++t;
        for (int i=t;i<=b;++i) ans.push_back(a[i][r]); --r;
        if (t<=b) for (int j=r;j>=l;--j) ans.push_back(a[b][j]); --b;
        if (l<=r) for (int i=b;i>=t;--i) ans.push_back(a[i][l]); ++l;
    }
    return ans;
}""",
        "py": """def spiral_order(a):
    ans = []
    while a:
        ans += a.pop(0)
        if a and a[0]:
            for row in a: ans.append(row.pop())
        if a: ans += a.pop()[::-1]
        if a and a[0]:
            for row in a[::-1]: ans.append(row.pop(0))
    return ans""",
    },
    {
        "slug": "07-linked-list",
        "title": "链表指针操作",
        "definition": "通过保存 next、重连指针和虚拟头结点，在 O(1) 额外空间完成链表修改。",
        "signals": ["反转、删除、合并", "快慢指针找位置或环", "头结点可能变化"],
        "steps": ["先保存当前节点的 next", "修改当前节点指向", "推进前驱与当前指针", "复杂删除优先加 dummy"],
        "example": "反转链表：1 → 2 → 3 变为 3 → 2 → 1",
        "visual": "linked_list",
        "hot": "Hot 100：206 反转链表｜141 环形链表｜21 合并有序链表｜25 K 个一组翻转｜146 LRU",
        "memory": "记忆：改指针前先保存 next；怕丢头就加 dummy",
        "cpp": """ListNode* reverseList(ListNode* head) {
    ListNode *prev = nullptr, *cur = head;
    while (cur) {
        ListNode* nxt = cur->next;
        cur->next = prev;
        prev = cur;
        cur = nxt;
    }
    return prev;
}""",
        "py": """def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev""",
    },
    {
        "slug": "08-binary-tree",
        "title": "二叉树 DFS / BFS",
        "definition": "DFS 适合递归求子树信息，BFS 适合按层处理；关键是明确函数返回值含义。",
        "signals": ["深度、路径、祖先、子树", "前中后序递归", "层序遍历 / 最短层数"],
        "steps": ["定义递归函数的返回含义", "处理空节点作为边界", "递归获取左右子树结果", "合并结果并返回当前节点答案"],
        "example": "最大深度：depth(node) = 1 + max(left, right)",
        "visual": "tree",
        "hot": "Hot 100：104 最大深度｜226 翻转二叉树｜102 层序遍历｜236 最近公共祖先｜124 最大路径和",
        "memory": "记忆：先问“子树能给我什么”，再写递归",
        "cpp": """int maxDepth(TreeNode* root) {
    if (!root) return 0;
    int left = maxDepth(root->left);
    int right = maxDepth(root->right);
    return 1 + max(left, right);
}""",
        "py": """def max_depth(root):
    if not root:
        return 0
    left = max_depth(root.left)
    right = max_depth(root.right)
    return 1 + max(left, right)""",
    },
    {
        "slug": "09-graph",
        "title": "图搜索（DFS / BFS / 拓扑）",
        "definition": "把节点与边建模后，用 visited 避免重复；连通块用 DFS/BFS，依赖关系用拓扑排序。",
        "signals": ["岛屿、连通块、扩散", "最短步数 / 分层搜索", "课程依赖与有向无环图"],
        "steps": ["确定节点、边和访问状态", "从未访问节点启动搜索", "访问邻居并标记 visited", "按连通块数或层数统计答案"],
        "example": "岛屿数量：遇到陆地就 DFS 淹没整个连通块",
        "visual": "graph",
        "hot": "Hot 100：200 岛屿数量｜994 腐烂的橘子｜207 课程表｜208 Trie",
        "memory": "记忆：图搜索先标记再入队/递归，避免重复访问",
        "cpp": """void dfs(vector<vector<char>>& g, int i, int j) {
    if (i<0||j<0||i==g.size()||j==g[0].size()||g[i][j]!='1') return;
    g[i][j] = '0';
    dfs(g,i+1,j); dfs(g,i-1,j); dfs(g,i,j+1); dfs(g,i,j-1);
}
int numIslands(vector<vector<char>>& g) {
    int ans=0;
    for(int i=0;i<g.size();++i) for(int j=0;j<g[0].size();++j)
        if(g[i][j]=='1') { ++ans; dfs(g,i,j); }
    return ans;
}""",
        "py": """def num_islands(g):
    def dfs(i, j):
        if not (0 <= i < len(g) and 0 <= j < len(g[0])) or g[i][j] != '1': return
        g[i][j] = '0'
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)): dfs(i+di, j+dj)
    ans = 0
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j] == '1': ans += 1; dfs(i, j)
    return ans""",
    },
    {
        "slug": "10-backtracking",
        "title": "回溯（Backtracking）",
        "definition": "在决策树上深度优先枚举：做选择、递归、撤销选择，并用剪枝减少无效分支。",
        "signals": ["所有组合 / 排列 / 切分", "棋盘放置与路径搜索", "答案是一组可行方案"],
        "steps": ["定义 path 表示当前选择", "满足条件时收集答案", "枚举本层可选项并剪枝", "递归后撤销刚才的选择"],
        "example": "子集：[1,2,3] 的每个元素都有“选 / 不选”两条分支",
        "visual": "backtracking",
        "hot": "Hot 100：46 全排列｜78 子集｜39 组合总和｜79 单词搜索｜51 N 皇后",
        "memory": "记忆：选择 → 递归 → 撤销；剪枝写在选择之前",
        "cpp": """void dfs(int i, vector<int>& a, vector<int>& path,
         vector<vector<int>>& ans) {
    ans.push_back(path);
    for (int j = i; j < a.size(); ++j) {
        path.push_back(a[j]);
        dfs(j + 1, a, path, ans);
        path.pop_back();
    }
}""",
        "py": """def subsets(a):
    ans, path = [], []
    def dfs(i):
        ans.append(path[:])
        for j in range(i, len(a)):
            path.append(a[j])
            dfs(j + 1)
            path.pop()
    dfs(0)
    return ans""",
    },
    {
        "slug": "11-binary-search",
        "title": "二分查找（Binary Search）",
        "definition": "在具有单调性的答案空间中，每次排除一半范围，时间复杂度 O(log n)。",
        "signals": ["有序数组", "存在单调真假边界", "寻找第一个 / 最后一个位置"],
        "steps": ["明确闭区间或左闭右开", "取 mid 并判断目标在哪侧", "保持区间定义不变地收缩", "循环结束返回边界位置"],
        "example": "搜索插入位置：[1,3,5,6]，target=2，答案为 1",
        "visual": "binary_search",
        "hot": "Hot 100：35 搜索插入位置｜34 查找首尾位置｜33 搜索旋转数组｜153 寻找最小值",
        "memory": "记忆：先写区间定义，再决定 while 与边界更新",
        "cpp": """int searchInsert(vector<int>& a, int target) {
    int l = 0, r = a.size();
    while (l < r) {
        int m = l + (r - l) / 2;
        if (a[m] < target) l = m + 1;
        else r = m;
    }
    return l;
}""",
        "py": """def search_insert(a, target):
    l, r = 0, len(a)
    while l < r:
        m = (l + r) // 2
        if a[m] < target: l = m + 1
        else: r = m
    return l""",
    },
    {
        "slug": "12-stack",
        "title": "栈（Stack）",
        "definition": "利用后进先出保存尚未完成的状态，适合括号匹配、嵌套结构与表达式解析。",
        "signals": ["最近打开的要最先关闭", "括号 / 嵌套 / 解码", "需要保存未处理状态"],
        "steps": ["遇到开放符号就入栈", "遇到关闭符号检查栈顶", "匹配则弹栈，否则失败", "结束时栈必须为空"],
        "example": "有效括号：([{}]) 按最近匹配顺序逐层弹栈",
        "visual": "stack",
        "hot": "Hot 100：20 有效的括号｜155 最小栈｜394 字符串解码",
        "memory": "记忆：处理嵌套结构时，栈顶就是最近的未完成任务",
        "cpp": """bool isValid(string s) {
    unordered_map<char,char> match{{')','('},{']','['},{'}','{'}};
    stack<char> st;
    for (char c : s) {
        if (!match.count(c)) st.push(c);
        else {
            if (st.empty() || st.top() != match[c]) return false;
            st.pop();
        }
    }
    return st.empty();
}""",
        "py": """def is_valid(s):
    match = {')':'(', ']':'[', '}':'{'}
    st = []
    for ch in s:
        if ch not in match: st.append(ch)
        elif not st or st.pop() != match[ch]:
            return False
    return not st""",
    },
    {
        "slug": "13-monotonic-stack",
        "title": "单调栈（Monotonic Stack）",
        "definition": "用栈维护候选下标的单调性，一次扫描找到每个元素左/右侧第一个更大或更小元素。",
        "signals": ["右侧第一个更大 / 更小", "每日温度、柱状图、接雨水", "每个元素最多入栈出栈一次"],
        "steps": ["从左到右扫描元素", "当前值破坏单调性时持续弹栈", "弹出的下标在此刻得到答案", "当前下标入栈；剩余元素无答案"],
        "example": "数组 [2, 1, 4, 3]：右侧第一个更大值为 [4, 4, -1, -1]",
        "visual": "monotonic_stack",
        "hot": "Hot 100：739 每日温度｜84 柱状图中最大的矩形｜42 接雨水",
        "memory": "记忆：找更大 → 维护递减栈；找更小 → 维护递增栈（栈存下标）",
        "cpp": """vector<int> nextGreater(vector<int>& a) {
    vector<int> ans(a.size(), -1), st;
    for (int i = 0; i < a.size(); ++i) {
        while (!st.empty() && a[i] > a[st.back()]) {
            ans[st.back()] = a[i];
            st.pop_back();
        }
        st.push_back(i);
    }
    return ans;
}""",
        "py": """def next_greater(a):
    ans, st = [-1] * len(a), []
    for i, x in enumerate(a):
        while st and x > a[st[-1]]:
            ans[st.pop()] = x
        st.append(i)
    return ans""",
    },
    {
        "slug": "14-heap",
        "title": "堆 / 优先队列（Heap）",
        "definition": "动态维护当前最小或最大元素，适合 Top K、流式数据和多路合并。",
        "signals": ["最大 / 最小的 K 个", "数据持续到达", "每次取当前最优元素"],
        "steps": ["选择最小堆或最大堆", "逐个加入候选元素", "堆大小超过 K 时弹出堆顶", "最终堆中保留所需 K 个"],
        "example": "数组第 K 大：维护大小为 K 的最小堆，堆顶就是答案",
        "visual": "heap",
        "hot": "Hot 100：215 数组第 K 大｜347 前 K 个高频元素｜295 数据流的中位数｜23 合并 K 链表",
        "memory": "记忆：求最大的 K 个，用大小为 K 的最小堆",
        "cpp": """int findKthLargest(vector<int>& a, int k) {
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int x : a) {
        pq.push(x);
        if (pq.size() > k) pq.pop();
    }
    return pq.top();
}""",
        "py": """import heapq

def find_kth_largest(a, k):
    heap = []
    for x in a:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]""",
    },
    {
        "slug": "15-greedy",
        "title": "贪心（Greedy）",
        "definition": "每一步选择当前局部最优，并证明该选择不会破坏全局最优解。",
        "signals": ["只关心当前最远 / 最早结束", "局部选择可持续扩展", "通常无需保存全部历史状态"],
        "steps": ["定义当前能达到的最优边界", "扫描所有可达位置", "用当前选择扩展边界", "边界无法覆盖当前位置则失败"],
        "example": "跳跃游戏：维护目前能到达的最远位置 farthest",
        "visual": "greedy",
        "hot": "Hot 100：121 买卖股票最佳时机｜55 跳跃游戏｜45 跳跃游戏 II｜763 划分字母区间",
        "memory": "记忆：贪心不只要“看起来最优”，还要有不后悔的理由",
        "cpp": """bool canJump(vector<int>& a) {
    int farthest = 0;
    for (int i = 0; i < a.size(); ++i) {
        if (i > farthest) return false;
        farthest = max(farthest, i + a[i]);
    }
    return true;
}""",
        "py": """def can_jump(a):
    farthest = 0
    for i, step in enumerate(a):
        if i > farthest:
            return False
        farthest = max(farthest, i + step)
    return True""",
    },
    {
        "slug": "16-dp-1d",
        "title": "一维动态规划（1D DP）",
        "definition": "把大问题拆成前缀状态，保存重复子问题答案，并按依赖顺序递推。",
        "signals": ["最优值 / 方案数", "当前答案依赖前几个状态", "暴力递归存在重复计算"],
        "steps": ["定义 dp[i] 的准确含义", "写出状态转移方程", "确定初始状态与遍历顺序", "按需压缩滚动变量"],
        "example": "打家劫舍：dp[i] = max(dp[i-1], dp[i-2] + nums[i])",
        "visual": "dp1",
        "hot": "Hot 100：70 爬楼梯｜198 打家劫舍｜279 完全平方数｜322 零钱兑换｜300 最长递增子序列",
        "memory": "记忆：DP 四件套：状态、转移、初始化、遍历顺序",
        "cpp": """int rob(vector<int>& a) {
    int prev2 = 0, prev1 = 0;
    for (int x : a) {
        int cur = max(prev1, prev2 + x);
        prev2 = prev1;
        prev1 = cur;
    }
    return prev1;
}""",
        "py": """def rob(a):
    prev2 = prev1 = 0
    for x in a:
        cur = max(prev1, prev2 + x)
        prev2, prev1 = prev1, cur
    return prev1""",
    },
    {
        "slug": "17-dp-2d",
        "title": "二维动态规划（2D DP）",
        "definition": "用二维状态描述两个维度或网格位置的子问题，如路径、两个字符串前缀或区间。",
        "signals": ["网格路径", "两个字符串比较", "状态同时依赖行与列"],
        "steps": ["定义 dp[i][j] 表示的子问题", "处理第一行 / 第一列边界", "从已知方向推导当前格", "按依赖方向遍历整张表"],
        "example": "最小路径和：dp[i][j] = grid[i][j] + min(上, 左)",
        "visual": "dp2",
        "hot": "Hot 100：62 不同路径｜64 最小路径和｜5 最长回文子串｜1143 LCS｜72 编辑距离",
        "memory": "记忆：二维 DP 先画表，再看每格从哪里来",
        "cpp": """int minPathSum(vector<vector<int>>& g) {
    int m=g.size(), n=g[0].size();
    for(int i=0;i<m;++i) for(int j=0;j<n;++j) {
        if(i==0 && j==0) continue;
        int up=i ? g[i-1][j] : INT_MAX;
        int left=j ? g[i][j-1] : INT_MAX;
        g[i][j] += min(up, left);
    }
    return g[m-1][n-1];
}""",
        "py": """def min_path_sum(g):
    for i in range(len(g)):
        for j in range(len(g[0])):
            if i == j == 0: continue
            up = g[i-1][j] if i else float('inf')
            left = g[i][j-1] if j else float('inf')
            g[i][j] += min(up, left)
    return g[-1][-1]""",
    },
    {
        "slug": "18-bit-tricks",
        "title": "位运算与数学技巧",
        "definition": "利用异或、位掩码、原地置换等性质，以 O(1) 额外空间解决特殊结构问题。",
        "signals": ["只出现一次 / 成对出现", "要求常数额外空间", "数字范围可映射到下标"],
        "steps": ["识别可利用的代数或下标性质", "选择 XOR / 位掩码 / 原地交换", "一次扫描累积或归位", "检查边界与重复值"],
        "example": "只出现一次的数字：x ^ x = 0，0 ^ y = y",
        "visual": "bit",
        "hot": "Hot 100：136 只出现一次的数字｜169 多数元素｜75 颜色分类｜31 下一个排列｜287 寻找重复数",
        "memory": "记忆：成对抵消优先想 XOR；值域对应下标优先想原地归位",
        "cpp": """int singleNumber(vector<int>& a) {
    int ans = 0;
    for (int x : a) ans ^= x;
    return ans;
}""",
        "py": """def single_number(a):
    ans = 0
    for x in a:
        ans ^= x
    return ans""",
    },
]


def zh(size, bold=False):
    return ImageFont.truetype(ZH_BOLD if bold else ZH_REG, size)


def mono(size, bold=False):
    return ImageFont.truetype(MONO, size, index=1 if bold else 0)


def center(draw, x, y, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((x - (box[2]-box[0])/2, y - (box[3]-box[1])/2), text, font=fnt, fill=fill)


def wrapped_lines(draw, text, fnt, width):
    lines, current = [], ""
    for ch in text:
        trial = current + ch
        if current and draw.textbbox((0, 0), trial, font=fnt)[2] > width:
            lines.append(current)
            current = ch
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def text_block(draw, xy, text, fnt, fill, width, spacing=7, max_lines=None):
    lines = wrapped_lines(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rounded_label(draw, box, text, fill=PALE, text_fill=BLUE, fnt=None):
    draw.rounded_rectangle(box, radius=12, fill=fill, outline="#A9CCF4", width=1)
    center(draw, (box[0]+box[2])/2, (box[1]+box[3])/2, text, fnt or zh(18, True), text_fill)


def draw_arrow(draw, start, end, color=BLUE, width=4):
    draw.line((start, end), fill=color, width=width)
    x1, y1 = start; x2, y2 = end
    if abs(x2-x1) >= abs(y2-y1):
        sign = 1 if x2 > x1 else -1
        pts = [(x2, y2), (x2-12*sign, y2-7), (x2-12*sign, y2+7)]
    else:
        sign = 1 if y2 > y1 else -1
        pts = [(x2, y2), (x2-7, y2-12*sign), (x2+7, y2-12*sign)]
    draw.polygon(pts, fill=color)


def draw_array(draw, values, x, y, cell=64, highlight=None, labels=None):
    highlight = highlight or {}
    for i, value in enumerate(values):
        x0 = x + i * cell
        fill = highlight.get(i, PALE2)
        draw.rounded_rectangle((x0, y, x0+cell-6, y+55), radius=10, fill=fill, outline=BLUE, width=2)
        center(draw, x0+(cell-6)/2, y+27, str(value), zh(22, True), NAVY)
        draw.text((x0+20, y+61), str(i), font=zh(15), fill=MUTED)
        if labels and i in labels:
            center(draw, x0+(cell-6)/2, y-22, labels[i], zh(17, True), labels[i] == "L" and GREEN or RED)


def draw_visual(draw, kind):
    x0, y0, x1, y1 = 62, 328, 1030, 670
    if kind == "hash":
        draw_array(draw, [2, 7, 11, 15], 115, 415, 110, {1: "#DFF5E9"})
        draw.text((118, 372), "扫描数组", font=zh(23, True), fill=NAVY)
        draw_arrow(draw, (540, 445), (635, 445))
        draw.text((650, 370), "哈希表：值 → 下标", font=zh(23, True), fill=NAVY)
        for i, (k, v) in enumerate([(2, 0), (7, 1)]):
            rounded_label(draw, (665, 420+i*68, 785, 468+i*68), str(k), "#DCEEFF")
            draw_arrow(draw, (790, 444+i*68), (850, 444+i*68), CYAN, 3)
            rounded_label(draw, (855, 420+i*68, 950, 468+i*68), str(v), "#FFF4D9", GOLD)
        draw.text((115, 535), "读到 7：need = 9 - 7 = 2，哈希表命中 2 → 返回 [0, 1]", font=zh(23), fill=GREEN)
    elif kind == "two_pointers":
        vals = [1,8,6,2,5,4,8,3,7]
        draw_array(draw, vals, 110, 515, 82, {1:"#DFF5E9",8:"#FFF0E5"}, {1:"L",8:"R"})
        base = 490
        scale = 25
        for i,v in enumerate(vals):
            x = 110+i*82+10
            draw.rectangle((x, base-v*scale, x+42, base), fill="#78B4F4", outline=BLUE)
        draw.rectangle((202, base-7*scale, 110+8*82+52, base), fill=(80,160,230,55), outline=CYAN, width=2)
        draw.text((305, 346), "面积 = min(8, 7) × (8 - 1) = 49", font=zh(28, True), fill=NAVY)
        draw.text((290, 390), "较短的是右侧 7 → 右指针左移", font=zh(23), fill=GREEN)
    elif kind == "window":
        chars = list("abcabcbb")
        draw_array(draw, chars, 170, 430, 90, {0:"#DFF5E9",1:"#DFF5E9",2:"#DFF5E9"}, {0:"L",2:"R"})
        draw.rounded_rectangle((160, 414, 430, 512), radius=16, outline=GREEN, width=4)
        draw.text((176, 355), "窗口 [L, R] = \"abc\"，无重复，长度 3", font=zh(27, True), fill=NAVY)
        draw.text((176, 555), "下一个字符 a 重复：先移动 L 删除旧 a，再扩张 R", font=zh(23), fill=GREEN)
    elif kind == "prefix":
        draw.text((130, 360), "原数组", font=zh(22, True), fill=NAVY)
        draw_array(draw, [1,1,1], 260, 350, 110)
        draw.text((130, 465), "前缀和", font=zh(22, True), fill=NAVY)
        draw_array(draw, [0,1,2,3], 260, 455, 110, {0:"#FFF4D9",2:"#DFF5E9",3:"#DFF5E9"})
        draw.text((260, 565), "pre - K 命中历史前缀和：2-2=0，3-2=1", font=zh(25, True), fill=GREEN)
        draw.text((260, 610), "对应区间 [0..1] 与 [1..2]", font=zh(22), fill=TEXT)
    elif kind == "intervals":
        axis_x, axis_y = 160, 600
        draw.line((axis_x,axis_y,930,axis_y), fill=NAVY, width=3)
        for i in range(1,11):
            x=axis_x+i*70; draw.line((x,axis_y-6,x,axis_y+6),fill=NAVY,width=2); center(draw,x,axis_y+25,str(i),zh(16),MUTED)
        rows=[(1,3,BLUE,430),(2,6,CYAN,480),(8,10,GOLD,530)]
        for l,r,c,y in rows:
            draw.line((axis_x+l*70,y,axis_x+r*70,y),fill=c,width=18)
            draw.ellipse((axis_x+l*70-9,y-9,axis_x+l*70+9,y+9),fill=c); draw.ellipse((axis_x+r*70-9,y-9,axis_x+r*70+9,y+9),fill=c)
        draw_arrow(draw,(430,390),(600,390),GREEN,4)
        draw.text((175,350), "排序后扫描", font=zh(25,True), fill=NAVY)
        draw.text((625,350), "重叠则扩展右端点", font=zh(25,True), fill=GREEN)
        draw.line((axis_x+70,650,axis_x+420,650),fill=GREEN,width=20); draw.text((600,632), "[1,6]",font=zh(22,True),fill=GREEN)
    elif kind == "matrix":
        vals=iter(range(1,10)); sx,sy=260,350; cell=80
        for i in range(3):
            for j in range(3):
                v=next(vals); draw.rounded_rectangle((sx+j*cell,sy+i*cell,sx+j*cell+66,sy+i*cell+66),radius=8,fill=PALE2,outline=BLUE,width=2); center(draw,sx+j*cell+33,sy+i*cell+33,str(v),zh(22,True),NAVY)
        path=[(293,383),(373,383),(453,383),(453,463),(453,543),(373,543),(293,543),(293,463),(373,463)]
        for a,b in zip(path,path[1:]): draw_arrow(draw,a,b,GREEN,4)
        draw.text((575,375), "遍历顺序", font=zh(25,True), fill=NAVY)
        draw.text((575,425), "1 → 2 → 3 → 6 → 9", font=zh(23), fill=TEXT)
        draw.text((575,470), "→ 8 → 7 → 4 → 5", font=zh(23), fill=TEXT)
        draw.text((575,535), "每走完一条边，就收缩对应边界", font=zh(23,True), fill=GREEN)
    elif kind == "linked_list":
        for row,y,rev in [("原链表",410,False),("反转后",545,True)]:
            draw.text((105,y+15),row,font=zh(23,True),fill=NAVY)
            vals=[1,2,3] if not rev else [3,2,1]
            for i,v in enumerate(vals):
                x=300+i*190; draw.ellipse((x,y,x+65,y+65),fill=PALE,outline=BLUE,width=3); center(draw,x+32,y+32,str(v),zh(24,True),NAVY)
                if i<2: draw_arrow(draw,(x+72,y+32),(x+175,y+32),GREEN,4)
            draw.text((875,y+16),"null",font=mono(20),fill=MUTED)
        draw.text((260,350), "保存 next → 改 cur.next → 整体向前推进", font=zh(26,True), fill=GREEN)
    elif kind == "tree":
        pts={1:(470,350),2:(320,450),3:(620,450),4:(245,565),5:(395,565),6:(545,565),7:(695,565)}
        for p,c in [(1,2),(1,3),(2,4),(2,5),(3,6),(3,7)]: draw.line((pts[p],pts[c]),fill="#8AB8EA",width=4)
        for v,(x,y) in pts.items(): draw.ellipse((x-32,y-32,x+32,y+32),fill=PALE if v!=1 else "#DFF5E9",outline=BLUE,width=3); center(draw,x,y,str(v),zh(22,True),NAVY)
        draw.text((760,370), "递归返回", font=zh(25,True),fill=NAVY)
        draw.text((760,420), "叶子深度 = 1", font=zh(22),fill=TEXT)
        draw.text((760,465), "节点 2 / 3 深度 = 2", font=zh(22),fill=TEXT)
        draw.text((760,510), "根节点深度 = 3", font=zh(24,True),fill=GREEN)
    elif kind == "graph":
        grid=[[1,1,0,0],[1,0,0,1],[0,0,1,1],[1,0,0,0]]; sx,sy=180,355; cell=68
        for i,row in enumerate(grid):
            for j,v in enumerate(row):
                fill="#7EB8F2" if v else "#EEF5FC"; draw.rounded_rectangle((sx+j*cell,sy+i*cell,sx+j*cell+55,sy+i*cell+55),radius=8,fill=fill,outline=BLUE,width=2)
        draw_arrow(draw,(485,475),(610,475),GREEN,4)
        draw.text((635,360), "遇到未访问陆地：", font=zh(24,True),fill=NAVY)
        draw.text((635,410), "① 岛屿数 +1", font=zh(23),fill=TEXT)
        draw.text((635,455), "② DFS/BFS 标记整块陆地", font=zh(23),fill=TEXT)
        draw.text((635,520), "本例共有 3 个连通块", font=zh(26,True),fill=GREEN)
    elif kind == "backtracking":
        levels=[[("[]",500)],[("[1]",300),("[]",700)],[("[1,2]",200),("[1]",400),("[2]",600),("[]",800)]]
        ys=[355,455,575]
        for li,level in enumerate(levels):
            for label,x in level:
                rounded_label(draw,(x-58,ys[li]-25,x+58,ys[li]+25),label,"#F4F9FF",NAVY,zh(18,True))
        for x in [300,700]: draw.line((500,380,x,430),fill="#8AB8EA",width=3)
        for x1,children in [(300,[200,400]),(700,[600,800])]:
            for x2 in children: draw.line((x1,480,x2,550),fill="#8AB8EA",width=3)
        draw.text((135,640), "每层：选择一个元素或跳过；递归返回时撤销 path 中的选择", font=zh(23,True),fill=GREEN)
    elif kind == "binary_search":
        vals=[1,3,5,6]; draw_array(draw,vals,260,430,125,{0:"#EEF5FC",1:"#FFF4D9",2:"#EEF5FC",3:"#EEF5FC"},{0:"L",2:"R"})
        draw.text((310,350), "target = 2，寻找第一个 ≥ 2 的位置", font=zh(26,True),fill=NAVY)
        draw.text((280,545), "mid=2，a[mid]=5 ≥ 2 → r=mid", font=zh(22),fill=TEXT)
        draw.text((280,590), "mid=1，a[mid]=3 ≥ 2 → r=mid → l=r=1", font=zh(22,True),fill=GREEN)
    elif kind == "stack":
        seq=list("([{}])"); draw_array(draw,seq,125,360,105)
        sx,sy=640,365
        for i,ch in enumerate(["(","[","{"]):
            y=sy+145-i*55; draw.rounded_rectangle((sx,y,sx+150,y+45),radius=8,fill=PALE,outline=BLUE,width=2); center(draw,sx+75,y+22,ch,zh(22,True),NAVY)
        draw.text((625,340), "栈顶", font=zh(20,True),fill=RED)
        draw.text((150,500), "读到 }：与栈顶 { 匹配，弹栈", font=zh(24,True),fill=GREEN)
        draw.text((150,555), "之后 ] 匹配 [，) 匹配 (，最终栈空 → 有效", font=zh(23),fill=TEXT)
    elif kind == "monotonic_stack":
        stages=[([0],"读 2：下标 0 入栈"),([0,1],"读 1：1 < 2，保持递减"),([2],"读 4：弹出 1、0，答案都为 4"),([2,3],"读 3：3 < 4，入栈")]
        xs=[80,315,555,805]
        for idx,(st,desc) in enumerate(stages):
            x=xs[idx]; draw.rounded_rectangle((x,355,x+205,600),radius=18,fill=(248,251,255,230),outline="#A6C9F1",width=2)
            rounded_label(draw,(x+35,375,x+170,415),f"i={idx}","#DCEEFF",NAVY,zh(18,True))
            for j,sidx in enumerate(st):
                yy=535-j*48; draw.rounded_rectangle((x+68,yy,x+138,yy+40),radius=7,fill=PALE,outline=BLUE,width=2); center(draw,x+103,yy+20,str(sidx),zh(20,True),NAVY)
            text_block(draw,(x+18,430),desc,zh(17),TEXT,170,5,3)
        draw.text((285,625), "最终答案：[4, 4, -1, -1]", font=zh(27,True),fill=GREEN)
    elif kind == "heap":
        pts=[(480,355),(360,455),(600,455),(300,555),(420,555),(540,555),(660,555)]; vals=[4,5,8,9,7,10,11]
        for p,c in [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]: draw.line((pts[p],pts[c]),fill="#8AB8EA",width=4)
        for (x,y),v in zip(pts,vals): draw.ellipse((x-30,y-30,x+30,y+30),fill="#FFF4D9" if v==4 else PALE,outline=BLUE,width=3); center(draw,x,y,str(v),zh(21,True),NAVY)
        draw.text((760,390), "大小固定为 K",font=zh(25,True),fill=NAVY)
        draw.text((760,445), "新元素入堆",font=zh(22),fill=TEXT)
        draw.text((760,490), "超过 K 就弹最小值",font=zh(22),fill=TEXT)
        draw.text((760,550), "堆顶 = 第 K 大",font=zh(25,True),fill=GREEN)
    elif kind == "greedy":
        vals=[2,3,1,1,4]; draw_array(draw,vals,180,455,120,{0:"#DFF5E9",1:"#DFF5E9",4:"#FFF4D9"})
        draw.text((200,360), "farthest 初始为 0",font=zh(24,True),fill=NAVY)
        draw_arrow(draw,(225,430),(570,430),GREEN,5); draw.text((310,390),"从 0 可到 2",font=zh(19),fill=GREEN)
        draw_arrow(draw,(345,565),(750,565),BLUE,5); draw.text((500,590),"扫描到 1 后可到 4",font=zh(19),fill=BLUE)
        draw.text((765,470), "最远位置覆盖终点 → true",font=zh(24,True),fill=GREEN)
    elif kind == "dp1":
        draw.text((145,350), "房屋金额",font=zh(22,True),fill=NAVY); draw_array(draw,[2,7,9,3,1],300,345,105)
        draw.text((145,465), "dp 最优值",font=zh(22,True),fill=NAVY); draw_array(draw,[2,7,11,11,12],300,460,105,{2:"#DFF5E9",4:"#FFF4D9"})
        draw.text((250,575), "当前位置：偷 = dp[i-2] + nums[i]；不偷 = dp[i-1]",font=zh(23),fill=TEXT)
        draw.text((370,620), "取两者最大值",font=zh(25,True),fill=GREEN)
    elif kind == "dp2":
        g=[[1,3,1],[1,5,1],[4,2,1]]; dp=[[1,4,5],[2,7,6],[6,8,7]]; sx,sy=165,350; cell=82
        for grid,ox,label in [(g,sx,"grid"),(dp,620,"dp")]:
            draw.text((ox+80,315),label,font=mono(22,True),fill=NAVY)
            for i,row in enumerate(grid):
                for j,v in enumerate(row):
                    fill="#DFF5E9" if (grid is dp and i==2 and j==2) else PALE2
                    draw.rounded_rectangle((ox+j*cell,sy+i*cell,ox+j*cell+66,sy+i*cell+66),radius=8,fill=fill,outline=BLUE,width=2); center(draw,ox+j*cell+33,sy+i*cell+33,str(v),zh(21,True),NAVY)
        draw_arrow(draw,(480,470),(585,470),GREEN,4)
        draw.text((260,610), "dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])",font=mono(18,True),fill=GREEN)
    elif kind == "bit":
        draw_array(draw,[4,1,2,1,2],160,410,130,{0:"#FFF4D9"})
        draw.text((200,350), "4 ^ 1 ^ 2 ^ 1 ^ 2",font=mono(25,True),fill=NAVY)
        draw.text((220,530), "= 4 ^ (1 ^ 1) ^ (2 ^ 2)",font=mono(23),fill=TEXT)
        draw.text((310,585), "= 4 ^ 0 ^ 0 = 4",font=mono(25,True),fill=GREEN)


def draw_code(draw, x, title, code, accent):
    draw.rounded_rectangle((x+10, 708, x+155, 742), radius=15, fill=accent)
    center(draw, x+82, 725, title, zh(19, True), WHITE)
    lines = code.splitlines()
    size = 9
    for candidate in range(16, 8, -1):
        test_font = mono(candidate)
        fits_width = all(draw.textbbox((0, 0), line, font=test_font)[2] <= 645 for line in lines)
        fits_height = len(lines) * (candidate + 4) <= 158
        if fits_width and fits_height:
            size = candidate
            break
    fnt = mono(size)
    line_height = size + 4
    y = 752
    for line in lines[:12]:
        draw.text((x+20, y), line, font=fnt, fill=TEXT)
        y += line_height


def render_card(card, index):
    img = Image.open(BASE).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")
    center(draw, 728, 72, card["title"], zh(48, True), NAVY)
    draw.line((310, 112, 1145, 112), fill=BLUE, width=3)

    draw.text((118, 158), "定义", font=zh(24, True), fill=NAVY)
    text_block(draw, (175, 156), card["definition"], zh(20), TEXT, 505, 5, 3)

    draw.text((810, 158), "识别信号", font=zh(24, True), fill=NAVY)
    for i, signal in enumerate(card["signals"]):
        draw.polygon([(820,191+i*28),(832,198+i*28),(820,205+i*28)],fill=BLUE)
        draw.text((842, 181+i*28), signal, font=zh(19, True if i == 0 else False), fill=TEXT if i else BLUE)

    draw.text((70, 292), "示例推演", font=zh(25, True), fill=NAVY)
    draw.text((205, 295), card["example"], font=zh(20), fill=TEXT)
    draw_visual(draw, card["visual"])

    draw.text((1115, 294), "算法步骤", font=zh(25, True), fill=NAVY)
    for i, step in enumerate(card["steps"]):
        cy = 356 + i * 80
        center(draw, 1090, cy, str(i+1), zh(21, True), WHITE)
        text_block(draw, (1120, cy-20), step, zh(19), TEXT, 255, 5, 2)

    draw_code(draw, 48, "C++", card["cpp"], NAVY)
    draw_code(draw, 738, "Python", card["py"], BLUE)

    center(draw, 728, 966, card["memory"], zh(22, True), NAVY)
    center(draw, 728, 1013, card["hot"], zh(17), TEXT)
    rounded_label(draw, (1280, 1030, 1380, 1062), f"{index:02d}/18", BLUE, WHITE, zh(16, True))
    path = OUT / f"{card['slug']}.png"
    img.convert("RGB").save(path, quality=96)


def make_preview():
    files = sorted(OUT.glob("[0-9][0-9]-*.png"))
    thumb_w, thumb_h, cols = 364, 272, 3
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (thumb_w * cols, thumb_h * rows), WHITE)
    for i, file in enumerate(files):
        im = Image.open(file).convert("RGB")
        im.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(im, ((i % cols) * thumb_w, (i // cols) * thumb_h))
    sheet.save(OUT / "hot100-method-cards-preview.png", quality=94)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for i, card in enumerate(CARDS, 1):
        render_card(card, i)
    make_preview()


if __name__ == "__main__":
    main()
