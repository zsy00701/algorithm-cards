# -*- coding: utf-8 -*-
"""代码随想录学习路线 36 个专题的方法卡内容（原创撰写，标准算法）。

字段与 hot100 模板一致：title/definition/signals/steps/example/hot/memory/cpp/py。
"""

CARDS = [
    {
        "title": "数组：二分查找",
        "definition": "在有序数组中每次比较中点并排除一半区间，O(log n) 定位目标或边界。",
        "signals": ["数组有序 / 答案具单调性", "查找某值或插入位置", "求第一个 / 最后一个满足条件"],
        "steps": ["确定区间定义（左闭右闭）", "取 mid，比较 a[mid] 与 target", "据结果收缩左界或右界", "循环结束返回位置或 -1"],
        "example": "[1,3,5,7,9] 查 7 → mid 收缩到下标 3",
        "hot": "代表题：704 二分查找｜35 搜索插入位置｜34 查找首尾位置",
        "memory": "记忆：先定区间，再据区间决定 while 与边界更新",
        "cpp": """int search(vector<int>& a, int target) {
    int l = 0, r = a.size() - 1;
    while (l <= r) {
        int m = l + (r - l) / 2;
        if (a[m] == target) return m;
        if (a[m] < target) l = m + 1;
        else r = m - 1;
    }
    return -1;
}""",
        "py": """def search(a, target):
    l, r = 0, len(a) - 1
    while l <= r:
        m = (l + r) // 2
        if a[m] == target:
            return m
        if a[m] < target: l = m + 1
        else: r = m - 1
    return -1""",
    },
    {
        "title": "数组：快慢双指针",
        "definition": "慢指针记录有效结果的写入位置，快指针扫描原数组，原地完成删除或筛选。",
        "signals": ["原地删除 / 去重", "保留满足条件的元素", "要求 O(1) 额外空间"],
        "steps": ["slow 指向下一个写入位", "fast 遍历每个元素", "符合条件则写入并 slow++", "返回 slow 即新长度"],
        "example": "移除元素 val：[3,2,2,3] 去 3 → [2,2]，返回 2",
        "hot": "代表题：27 移除元素｜26 删除有序数组重复项｜283 移动零",
        "memory": "记忆：slow 写、fast 读，原地覆盖",
        "cpp": """int removeElement(vector<int>& a, int val) {
    int slow = 0;
    for (int fast = 0; fast < a.size(); ++fast)
        if (a[fast] != val)
            a[slow++] = a[fast];
    return slow;
}""",
        "py": """def remove_element(a, val):
    slow = 0
    for fast in range(len(a)):
        if a[fast] != val:
            a[slow] = a[fast]
            slow += 1
    return slow""",
    },
    {
        "title": "数组：滑动窗口",
        "definition": "维护一个连续区间，右指针扩张、左指针收缩，在线性时间内求满足条件的最优窗口。",
        "signals": ["连续子数组 / 子串", "最长、最短或满足和条件", "窗口状态可增量维护"],
        "steps": ["右指针扩张并更新窗口和", "窗口满足条件时尝试收缩", "收缩时更新答案、移动左界", "扫描结束返回最优解"],
        "example": "长度最小子数组：和 ≥ s 的最短连续子数组",
        "hot": "代表题：209 长度最小的子数组｜76 最小覆盖子串｜904 水果成篮",
        "memory": "记忆：右扩张、左收缩，窗口始终保持合法",
        "cpp": """int minSubArrayLen(int s, vector<int>& a) {
    int l = 0, sum = 0, ans = INT_MAX;
    for (int r = 0; r < a.size(); ++r) {
        sum += a[r];
        while (sum >= s) {
            ans = min(ans, r - l + 1);
            sum -= a[l++];
        }
    }
    return ans == INT_MAX ? 0 : ans;
}""",
        "py": """def min_sub_array_len(s, a):
    l, sum_, ans = 0, 0, float('inf')
    for r, x in enumerate(a):
        sum_ += x
        while sum_ >= s:
            ans = min(ans, r - l + 1)
            sum_ -= a[l]; l += 1
    return 0 if ans == float('inf') else ans""",
    },
    {
        "title": "数组：前缀和",
        "definition": "预处理前缀和数组，使任意区间和转为两端前缀和之差，查询 O(1)。",
        "signals": ["多次区间求和查询", "区间和等于 K", "二维子矩阵求和"],
        "steps": ["构造 pre[i]=pre[i-1]+a[i]", "区间 [l,r] 和 = pre[r+1]-pre[l]", "配合哈希统计区间数量", "二维则按行列累加"],
        "example": "和为 K 的子数组：用前缀和 + 哈希计数",
        "hot": "代表题：303 区域和检索｜560 和为 K 的子数组｜304 二维区域和",
        "memory": "记忆：区间和 = pre[r+1] - pre[l]",
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
        "title": "数组：矩阵边界模拟",
        "definition": "用上下左右四条边界控制遍历顺序，每走完一条边就收缩对应边界。",
        "signals": ["螺旋遍历 / 生成", "按层处理二维矩阵", "方向固定但边界变化"],
        "steps": ["定义 top/bottom/left/right", "依次遍历上行、右列、下行、左列", "每条边后收缩边界", "转向前检查是否越界"],
        "example": "螺旋矩阵：右→下→左→上，逐层收缩",
        "hot": "代表题：59 螺旋矩阵 II｜54 螺旋矩阵｜48 旋转图像",
        "memory": "记忆：方向固定，边界收缩；转向前先判越界",
        "cpp": """vector<int> spiralOrder(vector<vector<int>>& m) {
    vector<int> r; if (m.empty()) return r;
    int t=0,b=m.size()-1,l=0,rt=m[0].size()-1;
    while (t<=b && l<=rt) {
        for (int j=l;j<=rt;++j) r.push_back(m[t][j]); ++t;
        for (int i=t;i<=b;++i) r.push_back(m[i][rt]); --rt;
        if (t<=b) for (int j=rt;j>=l;--j) r.push_back(m[b][j]); --b;
        if (l<=rt) for (int i=b;i>=t;--i) r.push_back(m[i][l]); ++l;
    }
    return r;
}""",
        "py": """def spiral_order(m):
    r = []
    while m:
        r += m.pop(0)
        if m and m[0]:
            for row in m: r.append(row.pop())
        if m: r += m.pop()[::-1]
        if m and m[0]:
            for row in m[::-1]: r.append(row.pop(0))
    return r""",
    },
    {
        "title": "链表：虚拟头结点",
        "definition": "在头部加一个 dummy 结点，使头结点的删除/插入与其他结点处理方式统一。",
        "signals": ["可能删除或修改头结点", "统一边界，少写特判", "需要返回新头结点"],
        "steps": ["建立 dummy->next = head", "用 cur 从 dummy 出发遍历", "按需修改 cur->next 指向", "返回 dummy->next"],
        "example": "删除值为 val 的所有结点，头也可能被删",
        "hot": "代表题：203 移除链表元素｜707 设计链表｜19 删除倒数第 N 个",
        "memory": "记忆：怕丢头、要改头 → 先加 dummy",
        "cpp": """ListNode* removeElements(ListNode* head, int val) {
    ListNode dummy(0); dummy.next = head;
    ListNode* cur = &dummy;
    while (cur->next) {
        if (cur->next->val == val)
            cur->next = cur->next->next;
        else cur = cur->next;
    }
    return dummy.next;
}""",
        "py": """def remove_elements(head, val):
    dummy = ListNode(0); dummy.next = head
    cur = dummy
    while cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return dummy.next""",
    },
    {
        "title": "链表：反转与重连",
        "definition": "遍历时先保存 next，再把当前结点指向前驱，逐步把链表方向翻转。",
        "signals": ["反转整段或局部链表", "两两交换、K 个一组", "需要重连指针"],
        "steps": ["prev=null, cur=head", "保存 nxt=cur->next", "cur->next=prev 翻转指向", "prev、cur 同步右移"],
        "example": "反转链表：1→2→3 变为 3→2→1",
        "hot": "代表题：206 反转链表｜92 反转链表 II｜24 两两交换",
        "memory": "记忆：改指针前先存 next，否则断链",
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
        "title": "链表：快慢指针与环",
        "definition": "快指针每次两步、慢指针一步；相遇判环，再次同速相遇即环入口。",
        "signals": ["判断链表是否有环", "找环的入口结点", "找中点 / 倒数第 K 个"],
        "steps": ["fast 走两步、slow 走一步", "相遇说明存在环", "一指针回头结点同速前进", "再次相遇处即环入口"],
        "example": "环形链表 II：相遇后从头与相遇点同速走",
        "hot": "代表题：141 环形链表｜142 环形链表 II｜876 链表中间结点",
        "memory": "记忆：快慢相遇判环，头与相遇点同速找入口",
        "cpp": """ListNode* detectCycle(ListNode* head) {
    ListNode *slow=head, *fast=head;
    while (fast && fast->next) {
        slow = slow->next; fast = fast->next->next;
        if (slow == fast) {
            ListNode* p = head;
            while (p != slow) { p=p->next; slow=slow->next; }
            return p;
        }
    }
    return nullptr;
}""",
        "py": """def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            p = head
            while p is not slow:
                p, slow = p.next, slow.next
            return p
    return None""",
    },
    {
        "title": "哈希表：集合、映射与计数",
        "definition": "用集合判存在、用映射存“键→信息”、用计数统计频次，把查找降到平均 O(1)。",
        "signals": ["快速判断是否出现", "配对 / 去重 / 计数", "用空间换时间"],
        "steps": ["明确 key 与要保存的值", "遍历时先查询所需 key", "命中则更新答案", "未命中则写入哈希表"],
        "example": "两数之和：查 target-x 是否已出现",
        "hot": "代表题：242 有效字母异位词｜349 两数组交集｜1 两数之和｜383 赎金信",
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
        "title": "字符串：反转、替换与旋转",
        "definition": "用双指针就地反转，配合“整体反转 + 局部反转”实现旋转等花式变换。",
        "signals": ["反转整串或区间", "按规则旋转字符串", "替换 / 去除空格"],
        "steps": ["双指针首尾交换实现反转", "旋转 = 先整体反转", "再分段局部反转", "注意边界与下标"],
        "example": "左旋字符串 k 位 = 反转前 k、反转后段、整体反转",
        "hot": "代表题：344 反转字符串｜541 反转字符串 II｜151 反转单词｜剑指58 左旋",
        "memory": "记忆：旋转三步走——整体反转 + 两段局部反转",
        "cpp": """string reverseLeftWords(string s, int k) {
    reverse(s.begin(), s.begin() + k);
    reverse(s.begin() + k, s.end());
    reverse(s.begin(), s.end());
    return s;
}""",
        "py": """def reverse_left_words(s, k):
    a = list(s)
    a[:k] = a[:k][::-1]
    a[k:] = a[k:][::-1]
    a.reverse()
    return ''.join(a)""",
    },
    {
        "title": "字符串：KMP 匹配",
        "definition": "预处理模式串的最长公共前后缀 next 数组，匹配失败时按 next 回退而不回退主串。",
        "signals": ["子串 / 模式匹配", "重复子串结构", "需要 O(n+m) 匹配"],
        "steps": ["构造 next（最长相等前后缀）", "主串指针不回退", "失配时模式串跳到 next[j-1]", "匹配完成返回起点"],
        "example": "在 aabaabaaf 中找 aabaaf",
        "hot": "代表题：28 找出字符串中第一个匹配项｜459 重复的子字符串",
        "memory": "记忆：next 记最长相等前后缀，失配按它回退",
        "cpp": """int strStr(string s, string p) {
    int n=p.size(); vector<int> nx(n,0);
    for (int i=1,j=0;i<n;++i){
        while(j&&p[i]!=p[j]) j=nx[j-1];
        if(p[i]==p[j]) ++j; nx[i]=j;
    }
    for (int i=0,j=0;i<s.size();++i){
        while(j&&s[i]!=p[j]) j=nx[j-1];
        if(s[i]==p[j]) ++j;
        if(j==n) return i-n+1;
    }
    return -1;
}""",
        "py": """def str_str(s, p):
    n = len(p); nx = [0]*n; j = 0
    for i in range(1, n):
        while j and p[i] != p[j]: j = nx[j-1]
        if p[i] == p[j]: j += 1
        nx[i] = j
    j = 0
    for i, ch in enumerate(s):
        while j and ch != p[j]: j = nx[j-1]
        if ch == p[j]: j += 1
        if j == n: return i - n + 1
    return -1""",
    },
    {
        "title": "栈与队列：相互模拟",
        "definition": "队列先进先出、栈后进先出；用两个栈可模拟队列，用两个队列可模拟栈。",
        "signals": ["要求用栈实现队列或反之", "倒腾元素改变出入顺序", "理解 FIFO 与 LIFO"],
        "steps": ["in 栈负责接收 push", "out 栈负责输出", "out 空时把 in 全部倒入", "peek/pop 从 out 取栈顶"],
        "example": "用两个栈实现队列的 push/pop/peek",
        "hot": "代表题：232 用栈实现队列｜225 用队列实现栈",
        "memory": "记忆：两栈模拟队列——out 空才从 in 倒灌",
        "cpp": """class MyQueue {
    stack<int> in, out;
    void move(){ while(!in.empty()){ out.push(in.top()); in.pop(); } }
public:
    void push(int x){ in.push(x); }
    int pop(){ if(out.empty()) move();
        int v=out.top(); out.pop(); return v; }
    int peek(){ if(out.empty()) move(); return out.top(); }
    bool empty(){ return in.empty()&&out.empty(); }
};""",
        "py": """class MyQueue:
    def __init__(self):
        self.inp, self.out = [], []
    def push(self, x): self.inp.append(x)
    def _move(self):
        if not self.out:
            while self.inp: self.out.append(self.inp.pop())
    def pop(self): self._move(); return self.out.pop()
    def peek(self): self._move(); return self.out[-1]""",
    },
    {
        "title": "栈：括号与逆波兰表达式",
        "definition": "用栈保存未完成的状态：左括号入栈等待匹配，运算数入栈等待运算符。",
        "signals": ["括号匹配 / 嵌套合法性", "逆波兰 / 表达式求值", "最近打开的最先关闭"],
        "steps": ["遇左括号 / 操作数入栈", "遇右括号检查栈顶是否匹配", "遇运算符弹出两数计算", "结束时栈应符合预期"],
        "example": "逆波兰：[\"2\",\"1\",\"+\",\"3\",\"*\"] = 9",
        "hot": "代表题：20 有效的括号｜1047 删除相邻重复项｜150 逆波兰表达式",
        "memory": "记忆：嵌套问题找栈，栈顶即最近未完成任务",
        "cpp": """int evalRPN(vector<string>& t) {
    stack<long> st;
    for (auto& s : t) {
        if (s=="+"||s=="-"||s=="*"||s=="/") {
            long b=st.top();st.pop(); long a=st.top();st.pop();
            st.push(s=="+"?a+b:s=="-"?a-b:s=="*"?a*b:a/b);
        } else st.push(stol(s));
    }
    return st.top();
}""",
        "py": """def eval_rpn(tokens):
    st, ops = [], {'+','-','*','/'}
    for s in tokens:
        if s in ops:
            b, a = st.pop(), st.pop()
            st.append({'+':a+b,'-':a-b,'*':a*b,
                       '/':int(a/b)}[s])
        else:
            st.append(int(s))
    return st[0]""",
    },
    {
        "title": "单调队列：滑动窗口最大值",
        "definition": "用双端队列维护单调递减的候选下标，队首始终是当前窗口最大值。",
        "signals": ["滑动窗口最值", "需要 O(n) 取窗口极值", "随窗口移动维护候选"],
        "steps": ["新元素入队前弹出更小的队尾", "下标入队尾", "队首超出窗口则弹出", "窗口成形后队首即最大值"],
        "example": "[1,3,-1,-3,5,3,6,7] k=3 → [3,3,5,5,6,7]",
        "hot": "代表题：239 滑动窗口最大值｜剑指59 队列最大值",
        "memory": "记忆：维护递减队列，队首即窗口最大值（存下标）",
        "cpp": """vector<int> maxSlidingWindow(vector<int>& a, int k) {
    deque<int> dq; vector<int> ans;
    for (int i = 0; i < a.size(); ++i) {
        while (!dq.empty() && a[dq.back()] < a[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() <= i - k) dq.pop_front();
        if (i >= k - 1) ans.push_back(a[dq.front()]);
    }
    return ans;
}""",
        "py": """from collections import deque

def max_sliding_window(a, k):
    dq, ans = deque(), []
    for i, x in enumerate(a):
        while dq and a[dq[-1]] < x: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()
        if i >= k - 1: ans.append(a[dq[0]])
    return ans""",
    },
    {
        "title": "堆：Top K 与优先队列",
        "definition": "用堆动态维护当前最值，求前 K 大用大小为 K 的小顶堆，堆顶即第 K 大。",
        "signals": ["最大 / 最小的 K 个", "前 K 高频元素", "数据流求中位数"],
        "steps": ["统计频次或读入元素", "维护大小为 K 的小顶堆", "超过 K 则弹出堆顶", "最终堆内即答案"],
        "example": "前 K 个高频元素：按频次建小顶堆取前 K",
        "hot": "代表题：347 前 K 个高频元素｜215 第 K 大｜23 合并 K 个链表",
        "memory": "记忆：求最大的 K 个，用大小为 K 的小顶堆",
        "cpp": """vector<int> topKFrequent(vector<int>& a, int k) {
    unordered_map<int,int> cnt;
    for (int x : a) ++cnt[x];
    priority_queue<pair<int,int>, vector<pair<int,int>>,
        greater<>> pq;
    for (auto& [v,c] : cnt) {
        pq.push({c, v});
        if (pq.size() > k) pq.pop();
    }
    vector<int> ans;
    while (!pq.empty()) { ans.push_back(pq.top().second); pq.pop(); }
    return ans;
}""",
        "py": """import heapq
from collections import Counter

def top_k_frequent(a, k):
    cnt = Counter(a)
    return [v for v, _ in
            heapq.nlargest(k, cnt.items(), key=lambda t: t[1])]""",
    },
    {
        "title": "二叉树：递归与迭代遍历",
        "definition": "递归天然对应前/中/后序；迭代用栈显式模拟，统一写法可用“标记法”。",
        "signals": ["前 / 中 / 后序遍历", "需要非递归实现", "按访问顺序处理结点"],
        "steps": ["递归：处理 + 左 + 右 调整顺序", "迭代：用栈保存待处理结点", "标记法：访问结点前压入 null", "弹出 null 后处理真正结点"],
        "example": "中序遍历：左 → 根 → 右",
        "hot": "代表题：144 前序｜94 中序｜145 后序｜统一迭代写法",
        "memory": "记忆：递归调顺序；迭代用栈，标记法统一三序",
        "cpp": """vector<int> inorder(TreeNode* root) {
    vector<int> ans; stack<TreeNode*> st;
    TreeNode* cur = root;
    while (cur || !st.empty()) {
        while (cur) { st.push(cur); cur = cur->left; }
        cur = st.top(); st.pop();
        ans.push_back(cur->val);
        cur = cur->right;
    }
    return ans;
}""",
        "py": """def inorder(root):
    ans, st, cur = [], [], root
    while cur or st:
        while cur:
            st.append(cur); cur = cur.left
        cur = st.pop()
        ans.append(cur.val)
        cur = cur.right
    return ans""",
    },
    {
        "title": "二叉树：层序遍历",
        "definition": "用队列按层处理结点，每轮取出当前层全部结点并把下一层入队（BFS）。",
        "signals": ["按层输出 / 统计", "每层最大值、平均值", "最短层数 / 右视图"],
        "steps": ["根结点入队", "记录当前队列长度 size", "弹出 size 个并收集本层", "其孩子入队，进入下一层"],
        "example": "层序遍历：逐层从左到右输出",
        "hot": "代表题：102 层序遍历｜199 右视图｜637 层平均值｜104 最大深度",
        "memory": "记忆：层序用队列，先记本层 size 再逐个弹",
        "cpp": """vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> ans; if (!root) return ans;
    queue<TreeNode*> q; q.push(root);
    while (!q.empty()) {
        int sz = q.size(); vector<int> level;
        for (int i = 0; i < sz; ++i) {
            auto* n = q.front(); q.pop();
            level.push_back(n->val);
            if (n->left) q.push(n->left);
            if (n->right) q.push(n->right);
        }
        ans.push_back(level);
    }
    return ans;
}""",
        "py": """from collections import deque

def level_order(root):
    ans = []
    if not root: return ans
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            n = q.popleft(); level.append(n.val)
            if n.left: q.append(n.left)
            if n.right: q.append(n.right)
        ans.append(level)
    return ans""",
    },
    {
        "title": "二叉树：属性、路径与构造",
        "definition": "用递归返回子树信息求深度、路径、公共祖先；用前序+中序等可唯一构造二叉树。",
        "signals": ["深度 / 直径 / 路径和", "最近公共祖先", "由遍历序列构造树"],
        "steps": ["明确递归函数返回的含义", "处理空结点边界", "递归取左右子树结果", "合并得到当前结点答案"],
        "example": "最大深度：depth = 1 + max(左, 右)",
        "hot": "代表题：104 最大深度｜236 最近公共祖先｜106 由中后序构造",
        "memory": "记忆：先想“子树能给我什么”，再写递归返回值",
        "cpp": """TreeNode* lca(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    TreeNode* l = lca(root->left, p, q);
    TreeNode* r = lca(root->right, p, q);
    if (l && r) return root;
    return l ? l : r;
}""",
        "py": """def lca(root, p, q):
    if not root or root is p or root is q:
        return root
    l = lca(root.left, p, q)
    r = lca(root.right, p, q)
    if l and r: return root
    return l or r""",
    },
    {
        "title": "二叉搜索树：中序有序性与增删查",
        "definition": "BST 左小右大，中序遍历得升序序列；查找、插入、删除均沿大小关系走单边。",
        "signals": ["有序性相关问题", "第 K 小 / 众数 / 验证 BST", "区间查找、增删结点"],
        "steps": ["利用 val 与根比较走左右", "查找 / 插入沿单边下降", "删除分 0/1/2 子结点讨论", "中序遍历可验证有序"],
        "example": "验证 BST：中序序列必须严格递增",
        "hot": "代表题：700 BST 查找｜98 验证 BST｜701 插入｜450 删除",
        "memory": "记忆：BST 的中序就是升序，善用单边走向",
        "cpp": """bool isValidBST(TreeNode* root, long lo=LONG_MIN,
                long hi=LONG_MAX) {
    if (!root) return true;
    if (root->val <= lo || root->val >= hi) return false;
    return isValidBST(root->left, lo, root->val) &&
           isValidBST(root->right, root->val, hi);
}""",
        "py": """def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))""",
    },
    {
        "title": "回溯：组合问题",
        "definition": "在决策树上枚举组合：用 start 控制起点避免重复，收集到目标长度即记录。",
        "signals": ["从 n 个里选 k 个", "组合而非排列（无顺序）", "答案是一组方案"],
        "steps": ["path 记录当前组合", "达到长度 k 时收集", "从 start 枚举候选", "递归后回撤 path"],
        "example": "组合：n=4,k=2 → [1,2][1,3]...[3,4]",
        "hot": "代表题：77 组合｜216 组合总和 III｜17 电话号码字母组合",
        "memory": "记忆：组合用 start 控制起点，避免重复选取",
        "cpp": """void dfs(int n,int k,int start,vector<int>& path,
         vector<vector<int>>& ans) {
    if (path.size()==k) { ans.push_back(path); return; }
    for (int i=start; i<=n; ++i) {
        path.push_back(i);
        dfs(n, k, i+1, path, ans);
        path.pop_back();
    }
}""",
        "py": """def combine(n, k):
    ans, path = [], []
    def dfs(start):
        if len(path) == k:
            ans.append(path[:]); return
        for i in range(start, n + 1):
            path.append(i)
            dfs(i + 1)
            path.pop()
    dfs(1)
    return ans""",
    },
    {
        "title": "回溯：子集与排列",
        "definition": "子集在每个结点都收集 path；排列用 used 标记已选元素并枚举所有位置。",
        "signals": ["求所有子集", "求全排列", "选 / 不选 或 顺序敏感"],
        "steps": ["子集：进入结点即记录 path", "排列：用 used 跳过已选", "枚举候选、递归、回撤", "叶子或满长度时收集"],
        "example": "子集：[1,2,3] 每个元素都有选/不选两支",
        "hot": "代表题：78 子集｜90 子集 II｜46 全排列｜47 全排列 II",
        "memory": "记忆：子集随时收，排列用 used 防重选",
        "cpp": """void dfs(vector<int>& a, vector<int>& path,
         vector<vector<int>>& ans) {
    ans.push_back(path);
    for (int i=0; i<a.size(); ++i) {
        if (!path.empty() && a[i] <= path.back()) continue;
        path.push_back(a[i]);
        dfs(a, path, ans);
        path.pop_back();
    }
}""",
        "py": """def permute(a):
    ans, path, used = [], [], [False]*len(a)
    def dfs():
        if len(path) == len(a):
            ans.append(path[:]); return
        for i, x in enumerate(a):
            if used[i]: continue
            used[i] = True; path.append(x)
            dfs()
            path.pop(); used[i] = False
    dfs()
    return ans""",
    },
    {
        "title": "回溯：剪枝与去重",
        "definition": "排序后用“同层去重”跳过相邻相同元素，并用边界剪枝提前砍掉无效分支。",
        "signals": ["含重复元素的组合 / 排列", "和为定值且不重复", "需要去掉重复方案"],
        "steps": ["先对候选数组排序", "同层 i>start 且 a[i]==a[i-1] 跳过", "和已超目标则 break 剪枝", "递归后回撤"],
        "example": "组合总和 II：含重复数，结果不能重复",
        "hot": "代表题：40 组合总和 II｜90 子集 II｜47 全排列 II",
        "memory": "记忆：排序 + 同层去重；剪枝写在进入分支前",
        "cpp": """void dfs(vector<int>& a,int target,int start,
         vector<int>& path, vector<vector<int>>& ans) {
    if (target==0) { ans.push_back(path); return; }
    for (int i=start; i<a.size() && a[i]<=target; ++i) {
        if (i>start && a[i]==a[i-1]) continue;
        path.push_back(a[i]);
        dfs(a, target-a[i], i+1, path, ans);
        path.pop_back();
    }
}""",
        "py": """def combination_sum2(a, target):
    a.sort(); ans, path = [], []
    def dfs(start, rest):
        if rest == 0:
            ans.append(path[:]); return
        for i in range(start, len(a)):
            if a[i] > rest: break
            if i > start and a[i] == a[i-1]: continue
            path.append(a[i])
            dfs(i + 1, rest - a[i])
            path.pop()
    dfs(0, target)
    return ans""",
    },
    {
        "title": "回溯：棋盘搜索",
        "definition": "在二维棋盘上逐行/逐格放置并校验约束，冲突即回撤，典型如 N 皇后、解数独。",
        "signals": ["二维放置问题", "行列 / 对角线约束", "填格 + 合法性校验"],
        "steps": ["按行（或格）递归放置", "放置前校验是否合法", "合法则递归下一行", "失败回撤当前放置"],
        "example": "N 皇后：每行放一个，校验列与两对角线",
        "hot": "代表题：51 N 皇后｜37 解数独｜79 单词搜索",
        "memory": "记忆：逐行放置 + 约束校验，冲突即回撤",
        "cpp": """bool valid(vector<string>& b,int r,int c,int n){
    for(int i=0;i<r;++i) if(b[i][c]=='Q') return false;
    for(int i=r-1,j=c-1;i>=0&&j>=0;--i,--j)
        if(b[i][j]=='Q') return false;
    for(int i=r-1,j=c+1;i>=0&&j<n;--i,++j)
        if(b[i][j]=='Q') return false;
    return true;
}""",
        "py": """def solve_n_queens(n):
    ans, board = [], [['.']*n for _ in range(n)]
    cols, d1, d2 = set(), set(), set()
    def dfs(r):
        if r == n:
            ans.append([''.join(x) for x in board]); return
        for c in range(n):
            if c in cols or r-c in d1 or r+c in d2: continue
            board[r][c]='Q'; cols.add(c); d1.add(r-c); d2.add(r+c)
            dfs(r+1)
            board[r][c]='.'; cols.discard(c); d1.discard(r-c); d2.discard(r+c)
    dfs(0)
    return ans""",
    },
    {
        "title": "贪心：序列与局部最优",
        "definition": "每步取当前局部最优并论证不破坏全局最优，常以一次扫描维护最优边界。",
        "signals": ["跳跃 / 加油站 / 分发", "维护当前最远或最优", "无需保存全部历史"],
        "steps": ["定义当前可达 / 最优边界", "扫描时用当前元素更新边界", "判断能否覆盖目标位置", "得出可行性或最优值"],
        "example": "跳跃游戏：维护能到达的最远位置",
        "hot": "代表题：455 分发饼干｜55 跳跃游戏｜53 最大子数组和｜134 加油站",
        "memory": "记忆：贪心要有“不后悔”的理由，否则用 DP",
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
        "title": "贪心：区间问题",
        "definition": "按起点或终点排序，再贪心地合并、保留或删除区间，避免两两比较。",
        "signals": ["区间重叠 / 合并", "无重叠区间最多保留", "用最少箭引爆气球"],
        "steps": ["按左端或右端排序", "维护上一个区间的边界", "重叠则合并 / 计数删除", "不重叠则更新边界"],
        "example": "合并区间：[1,3][2,6][8,10] → [1,6][8,10]",
        "hot": "代表题：56 合并区间｜435 无重叠区间｜452 引爆气球｜763 划分字母区间",
        "memory": "记忆：区间题先排序，再只盯“上一个区间”",
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
        "title": "动态规划：基础与网格",
        "definition": "把问题拆成子问题并保存结果按依赖递推；网格 DP 中每格答案由上方与左方转移而来。",
        "signals": ["计数 / 最优路径", "当前状态依赖前若干状态", "暴力递归存在重叠子问题"],
        "steps": ["定义 dp 的准确含义", "写出状态转移方程", "初始化边界（首行首列）", "按依赖顺序遍历填表"],
        "example": "不同路径：dp[i][j]=dp[i-1][j]+dp[i][j-1]",
        "hot": "代表题：509 斐波那契｜62 不同路径｜64 最小路径和｜70 爬楼梯",
        "memory": "记忆：DP 四件套——状态、转移、初始化、遍历顺序",
        "cpp": """int uniquePaths(int m, int n) {
    vector<vector<int>> dp(m, vector<int>(n, 1));
    for (int i = 1; i < m; ++i)
        for (int j = 1; j < n; ++j)
            dp[i][j] = dp[i-1][j] + dp[i][j-1];
    return dp[m-1][n-1];
}""",
        "py": """def unique_paths(m, n):
    dp = [[1]*n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]""",
    },
    {
        "title": "动态规划：01 背包",
        "definition": "每件物品只能选一次；用一维 dp 时容量必须倒序遍历，避免一件物品被重复选。",
        "signals": ["选 / 不选，容量受限", "能否凑出目标和", "求最大价值 / 方案数"],
        "steps": ["dp[j] = 容量 j 的最优值", "外层遍历物品", "内层容量倒序到 w[i]", "dp[j]=max(dp[j],dp[j-w]+v)"],
        "example": "分割等和子集：能否选出和为 sum/2",
        "hot": "代表题：416 分割等和子集｜1049 最后石头重量 II｜494 目标和",
        "memory": "记忆：01 背包一维时，容量必须倒序遍历",
        "cpp": """bool canPartition(vector<int>& a) {
    int sum=accumulate(a.begin(),a.end(),0);
    if (sum&1) return false;
    int t=sum/2; vector<int> dp(t+1,0);
    for (int x : a)
        for (int j=t; j>=x; --j)
            dp[j]=max(dp[j], dp[j-x]+x);
    return dp[t]==t;
}""",
        "py": """def can_partition(a):
    s = sum(a)
    if s % 2: return False
    t = s // 2
    dp = [0]*(t+1)
    for x in a:
        for j in range(t, x-1, -1):
            dp[j] = max(dp[j], dp[j-x] + x)
    return dp[t] == t""",
    },
    {
        "title": "动态规划：完全背包",
        "definition": "每件物品可选无限次；一维 dp 容量正序遍历即可重复选取同一物品。",
        "signals": ["物品可重复使用", "凑金额 / 爬楼梯方案", "求最少个数或方案数"],
        "steps": ["dp[j] = 容量 j 的最优解", "外层物品、内层容量正序", "求组合数：先物品后容量", "求排列数：先容量后物品"],
        "example": "零钱兑换：凑出 amount 的最少硬币数",
        "hot": "代表题：322 零钱兑换｜518 零钱兑换 II｜279 完全平方数",
        "memory": "记忆：完全背包容量正序；组合先物品、排列先容量",
        "cpp": """int coinChange(vector<int>& coins, int amount) {
    vector<int> dp(amount+1, amount+1); dp[0]=0;
    for (int c : coins)
        for (int j=c; j<=amount; ++j)
            dp[j] = min(dp[j], dp[j-c]+1);
    return dp[amount]>amount ? -1 : dp[amount];
}""",
        "py": """def coin_change(coins, amount):
    INF = amount + 1
    dp = [0] + [INF]*amount
    for c in coins:
        for j in range(c, amount + 1):
            dp[j] = min(dp[j], dp[j-c] + 1)
    return -1 if dp[amount] > amount else dp[amount]""",
    },
    {
        "title": "动态规划：打家劫舍",
        "definition": "相邻不能同时选：每个位置在“偷（含前前）”与“不偷（取前一个）”间取较大值。",
        "signals": ["相邻元素互斥", "环形或树形变体", "求最大累计收益"],
        "steps": ["dp[i]=max(dp[i-1],dp[i-2]+a[i])", "用两个变量滚动压缩", "环形拆成两段分别求", "树形则后序返回偷/不偷"],
        "example": "打家劫舍：dp[i]=max(dp[i-1],dp[i-2]+nums[i])",
        "hot": "代表题：198 打家劫舍｜213 打家劫舍 II｜337 打家劫舍 III",
        "memory": "记忆：偷不偷取大者；环形拆两段，树形后序返回二元组",
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
        "title": "动态规划：股票状态机",
        "definition": "用“持有 / 不持有”等状态描述每天的最优收益，按状态转移方程逐日递推。",
        "signals": ["买卖股票系列", "限次数 / 含冷冻期 / 手续费", "状态在持有与空仓间转移"],
        "steps": ["定义 hold / cash 状态", "hold=max(hold, cash-price)", "cash=max(cash, hold+price)", "按约束加冷冻期或次数维度"],
        "example": "可多次交易：每天在买入/卖出间取优",
        "hot": "代表题：121/122 买卖股票｜123/188 限次数｜309 冷冻期｜714 手续费",
        "memory": "记忆：先画状态机，再写每天 hold/cash 转移",
        "cpp": """int maxProfit(vector<int>& p) {
    int hold = INT_MIN, cash = 0;
    for (int x : p) {
        hold = max(hold, cash - x);
        cash = max(cash, hold + x);
    }
    return cash;
}""",
        "py": """def max_profit(prices):
    hold, cash = float('-inf'), 0
    for x in prices:
        hold = max(hold, cash - x)
        cash = max(cash, hold + x)
    return cash""",
    },
    {
        "title": "动态规划：子序列与编辑距离",
        "definition": "用二维 dp[i][j] 表示两串前缀的关系；字符相等时继承对角线，否则取邻格最优。",
        "signals": ["公共子序列 / 子串", "编辑距离 / 删除操作", "两个字符串比较"],
        "steps": ["dp[i][j] 表示前缀 i、j 的解", "字符相等取 dp[i-1][j-1]+1", "不等取相邻状态最优", "初始化第一行与第一列"],
        "example": "最长公共子序列 LCS",
        "hot": "代表题：300 最长递增子序列｜1143 LCS｜72 编辑距离｜583 删除操作",
        "memory": "记忆：相等走对角线，不等取邻格最优",
        "cpp": """int minDistance(string a, string b) {
    int m=a.size(), n=b.size();
    vector<vector<int>> dp(m+1, vector<int>(n+1));
    for (int i=0;i<=m;++i) dp[i][0]=i;
    for (int j=0;j<=n;++j) dp[0][j]=j;
    for (int i=1;i<=m;++i) for (int j=1;j<=n;++j)
        dp[i][j] = a[i-1]==b[j-1] ? dp[i-1][j-1]
            : 1+min({dp[i-1][j],dp[i][j-1],dp[i-1][j-1]});
    return dp[m][n];
}""",
        "py": """def min_distance(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1],
                                     dp[i-1][j-1])
    return dp[m][n]""",
    },
    {
        "title": "动态规划：回文问题",
        "definition": "用区间 dp[i][j] 表示子串 i..j 是否回文；由内向外扩展，相等且内部回文则成立。",
        "signals": ["最长回文子串 / 子序列", "回文划分计数", "区间型状态"],
        "steps": ["dp[i][j]：s[i..j] 是否回文", "s[i]==s[j] 且内部回文则真", "i 倒序、j 正序遍历", "记录最长区间长度"],
        "example": "最长回文子串：中心扩展或区间 DP",
        "hot": "代表题：5 最长回文子串｜516 最长回文子序列｜647 回文子串",
        "memory": "记忆：区间 DP 由内向外，i 倒序、j 正序",
        "cpp": """string longestPalindrome(string s) {
    int n=s.size(), st=0, len=1;
    vector<vector<bool>> dp(n, vector<bool>(n,false));
    for (int i=n-1;i>=0;--i) for (int j=i;j<n;++j)
        if (s[i]==s[j] && (j-i<2 || dp[i+1][j-1])) {
            dp[i][j]=true;
            if (j-i+1>len){ len=j-i+1; st=i; }
        }
    return s.substr(st, len);
}""",
        "py": """def longest_palindrome(s):
    n = len(s); start, length = 0, 1
    dp = [[False]*n for _ in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(i, n):
            if s[i]==s[j] and (j-i < 2 or dp[i+1][j-1]):
                dp[i][j] = True
                if j-i+1 > length:
                    length, start = j-i+1, i
    return s[start:start+length]""",
    },
    {
        "title": "单调栈：下一个更大元素与柱状图",
        "definition": "栈内保存候选下标并维持单调，遇到破坏单调的元素时弹栈结算答案，一次扫描完成。",
        "signals": ["右 / 左侧第一个更大或更小", "每日温度、接雨水", "柱状图最大矩形"],
        "steps": ["从左到右扫描元素", "破坏单调性时持续弹栈", "弹出下标此刻得到答案", "当前下标入栈"],
        "example": "每日温度：求右侧第一个更高温度的间隔",
        "hot": "代表题：739 每日温度｜496 下一个更大元素｜84 柱状图最大矩形｜42 接雨水",
        "memory": "记忆：找更大→维护递减栈；找更小→递增栈（存下标）",
        "cpp": """vector<int> dailyTemperatures(vector<int>& t) {
    vector<int> ans(t.size(), 0), st;
    for (int i = 0; i < t.size(); ++i) {
        while (!st.empty() && t[i] > t[st.back()]) {
            ans[st.back()] = i - st.back();
            st.pop_back();
        }
        st.push_back(i);
    }
    return ans;
}""",
        "py": """def daily_temperatures(t):
    ans, st = [0]*len(t), []
    for i, x in enumerate(t):
        while st and x > t[st[-1]]:
            j = st.pop()
            ans[j] = i - j
        st.append(i)
    return ans""",
    },
    {
        "title": "图论：DFS/BFS 与岛屿",
        "definition": "把网格 / 邻接关系建模为图，用 visited 防重复；连通块用 DFS/BFS 淹没或分层扩散。",
        "signals": ["岛屿 / 连通块计数", "最短步数 / 多源扩散", "网格四方向遍历"],
        "steps": ["遍历每个未访问结点", "遇陆地启动一次搜索", "递归 / 入队四方向邻居", "标记访问，统计块数或层数"],
        "example": "岛屿数量：遇到陆地就 DFS 淹没整块",
        "hot": "代表题：200 岛屿数量｜695 岛屿最大面积｜994 腐烂的橘子",
        "memory": "记忆：先标记再递归 / 入队，避免重复访问",
        "cpp": """void dfs(vector<vector<char>>& g,int i,int j){
    if(i<0||i>=g.size()||j<0||j>=g[0].size()||g[i][j]!='1') return;
    g[i][j]='0';
    dfs(g,i+1,j); dfs(g,i-1,j); dfs(g,i,j+1); dfs(g,i,j-1);
}
int numIslands(vector<vector<char>>& g){
    int ans=0;
    for(int i=0;i<g.size();++i) for(int j=0;j<g[0].size();++j)
        if(g[i][j]=='1'){ ++ans; dfs(g,i,j); }
    return ans;
}""",
        "py": """def num_islands(g):
    def dfs(i, j):
        if not (0<=i<len(g) and 0<=j<len(g[0])) or g[i][j]!='1':
            return
        g[i][j] = '0'
        for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):
            dfs(i+di, j+dj)
    ans = 0
    for i in range(len(g)):
        for j in range(len(g[0])):
            if g[i][j] == '1':
                ans += 1; dfs(i, j)
    return ans""",
    },
    {
        "title": "图论：并查集、拓扑排序与最小生成树",
        "definition": "并查集维护连通性，拓扑排序按入度处理依赖，MST（Kruskal/Prim）求最小连接代价。",
        "signals": ["判断连通 / 是否成环", "课程依赖 / 任务排序", "最小连接所有点的代价"],
        "steps": ["并查集：find 路径压缩 + union", "拓扑：入度为 0 入队、逐个删边", "Kruskal：按边权排序 + 并查集", "Prim：从已选集合扩展最近边"],
        "example": "课程表：拓扑排序判断能否修完",
        "hot": "代表题：547 省份数量｜207 课程表｜1584 连接点最小费用",
        "memory": "记忆：连通用并查集、依赖用拓扑、最小连接用 MST",
        "cpp": """struct DSU {
    vector<int> f;
    DSU(int n): f(n) { iota(f.begin(), f.end(), 0); }
    int find(int x){ return f[x]==x ? x : f[x]=find(f[x]); }
    void uni(int a,int b){ f[find(a)] = find(b); }
};""",
        "py": """class DSU:
    def __init__(self, n):
        self.f = list(range(n))
    def find(self, x):
        if self.f[x] != x:
            self.f[x] = self.find(self.f[x])
        return self.f[x]
    def union(self, a, b):
        self.f[self.find(a)] = self.find(b)""",
    },
    {
        "title": "图论：最短路径",
        "definition": "Dijkstra 解非负权单源最短路（堆优化），Bellman-Ford 容忍负权，Floyd 解多源。",
        "signals": ["带权图最短距离", "非负权用 Dijkstra", "负权 / 多源用 BF / Floyd"],
        "steps": ["dist 初始化为无穷、起点 0", "小顶堆取当前最近结点", "松弛其所有邻边", "出堆即得最终最短距离"],
        "example": "Dijkstra：堆优化逐步确定最近点",
        "hot": "代表题：743 网络延迟时间｜787 K 站中转｜1631 最小体力路径",
        "memory": "记忆：非负权 Dijkstra+堆；负权 BF；多源 Floyd",
        "cpp": """vector<int> dijkstra(int n,
        vector<vector<pair<int,int>>>& g, int s) {
    vector<int> d(n, INT_MAX); d[s]=0;
    priority_queue<pair<int,int>, vector<pair<int,int>>,
        greater<>> pq; pq.push({0,s});
    while (!pq.empty()) {
        auto [dist,u]=pq.top(); pq.pop();
        if (dist>d[u]) continue;
        for (auto [v,w]:g[u]) if (d[u]+w<d[v]) {
            d[v]=d[u]+w; pq.push({d[v],v});
        }
    }
    return d;
}""",
        "py": """import heapq

def dijkstra(n, g, s):
    d = [float('inf')]*n; d[s] = 0
    pq = [(0, s)]
    while pq:
        dist, u = heapq.heappop(pq)
        if dist > d[u]: continue
        for v, w in g[u]:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
                heapq.heappush(pq, (d[v], v))
    return d""",
    },
]
