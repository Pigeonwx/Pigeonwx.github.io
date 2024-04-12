# 快手算法题

[TOC]

# 快手秋招真题在手-leetcode

> 来源：力扣（LeetCode）



## 一、矩阵

### 回文链表-E

#### 题目

给你一个单链表的头节点 `head` ，请你判断该链表是否为回文链表。如果是，返回 `true` ；否则，返回 `false` 。



#### 解答

```java
class Solution {
    public boolean isPalindrome(ListNode head) {
        List<Integer> vals = new ArrayList<Integer>();

        // 将链表的值复制到数组中
        ListNode currentNode = head;
        while (currentNode != null) {
            vals.add(currentNode.val);
            currentNode = currentNode.next;
        }

        // 使用双指针判断是否回文
        int front = 0;
        int back = vals.size() - 1;
        while (front < back) {
            if (!vals.get(front).equals(vals.get(back))) {
                return false;
            }
            front++;
            back--;
        }
        return true
          
    }
}
```



### 合并两个有序数组-E

#### 题目

给你两个按 **非递减顺序** 排列的整数数组 `nums1` 和 `nums2`，另有两个整数 `m` 和 `n` ，分别表示 `nums1` 和 `nums2` 中的元素数目。

请你 **合并** `nums2` 到 `nums1` 中，使合并后的数组同样按 **非递减顺序** 排列。

**注意：**最终，合并后数组不应由函数返回，而是存储在数组 `nums1` 中。为了应对这种情况，`nums1` 的初始长度为 `m + n`，其中前 `m` 个元素表示应合并的元素，后 `n` 个元素为 `0` ，应忽略。`nums2` 的长度为 `n` 。

 

**示例 1：**

```
输入：nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
输出：[1,2,2,3,5,6]
解释：需要合并 [1,2,3] 和 [2,5,6] 。
合并结果是 [1,2,2,3,5,6] ，其中斜体加粗标注的为 nums1 中的元素。
```

**示例 2：**

```
输入：nums1 = [1], m = 1, nums2 = [], n = 0
输出：[1]
解释：需要合并 [1] 和 [] 。
合并结果是 [1] 。
```



#### 解答

```java
class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        int k=m+n-1;
        int i=m-1,j=n-1;
        while(k>=0){
            if(i>=0&&(j<0||nums1[i]>nums2[j])){
                nums1[k--]=nums1[i--];
            }else if (j>=0&&(i<0||nums1[i]<=nums2[j])){
                nums1[k--]=nums2[j--];
            }else{
                break;
            }
        }
    }
}
```



### 恢复二叉搜索树-M

#### 题目



#### 解答

```java
class Solution {
    public void recoverTree(TreeNode root) {
        List<Integer> nums = new ArrayList<Integer>();
        inorder(root, nums);
        int[] swapped = findTwoSwapped(nums);
        recover(root, 2, swapped[0], swapped[1]);
    }

    public void inorder(TreeNode root, List<Integer> nums) {
        if (root == null) {
            return;
        }
        inorder(root.left, nums);
        nums.add(root.val);
        inorder(root.right, nums);
    }

    public int[] findTwoSwapped(List<Integer> nums) {
        int n = nums.size();
        int index1 = -1, index2 = -1;
        for (int i = 0; i < n - 1; ++i) {
            if (nums.get(i + 1) < nums.get(i)) {
                index2 = i + 1;
                if (index1 == -1) {
                    index1 = i;
                } else {
                    break;
                }
            }
        }
        int x = nums.get(index1), y = nums.get(index2);
        return new int[]{x, y};
    }

    public void recover(TreeNode root, int count, int x, int y) {
        if (root != null) {
            if (root.val == x || root.val == y) {
                root.val = root.val == x ? y : x;
                if (--count == 0) {
                    return;
                }
            }
            recover(root.right, count, x, y);
            recover(root.left, count, x, y);
        }
    }
}

```



### 分汤-M

#### 题目

有 **A 和 B 两种类型** 的汤。一开始每种类型的汤有 `n` 毫升。有四种分配操作：

1. 提供 `100ml` 的 **汤A** 和 `0ml` 的 **汤B** 。
2. 提供 `75ml` 的 **汤A** 和 `25ml` 的 **汤B** 。
3. 提供 `50ml` 的 **汤A** 和 `50ml` 的 **汤B** 。
4. 提供 `25ml` 的 **汤A** 和 `75ml` 的 **汤B** 。

当我们把汤分配给某人之后，汤就没有了。每个回合，我们将从四种概率同为 `0.25` 的操作中进行分配选择。如果汤的剩余量不足以完成某次操作，我们将尽可能分配。当两种类型的汤都分配完时，停止操作。

**注意** 不存在先分配 `100` ml **汤B** 的操作。

需要返回的值： **汤A** 先分配完的概率 + **汤A和汤B** 同时分配完的概率 / 2。返回值在正确答案 `10-5` 的范围内将被认为是正确的。

 

**示例 1:**

```
输入: n = 50
输出: 0.62500
解释:如果我们选择前两个操作，A 首先将变为空。
对于第三个操作，A 和 B 会同时变为空。
对于第四个操作，B 首先将变为空。
所以 A 变为空的总概率加上 A 和 B 同时变为空的概率的一半是 0.25 *(1 + 1 + 0.5 + 0)= 0.625。
```

#### 解答

```java
class Solution {
    public double soupServings(int n) {
        n = (int) Math.ceil((double) n / 25);
        if (n >= 179) {
            return 1.0;
        }
        double[][] dp = new double[n + 1][n + 1];
        dp[0][0] = 0.5;
        for (int i = 1; i <= n; i++) {
            dp[0][i] = 1.0;
        }
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                dp[i][j] = (dp[Math.max(0, i - 4)][j] + dp[Math.max(0, i - 3)][Math.max(0, j - 1)] + dp[Math.max(0, i - 2)][Math.max(0, j - 2)] + dp[Math.max(0, i - 1)][Math.max(0, j - 3)]) / 4.0;
            }
        }
        return dp[n][n];
    }
}
```



### 矩阵置零-M

#### 题目

给定一个 `*m* x *n*` 的矩阵，如果一个元素为 **0** ，则将其所在行和列的所有元素都设为 **0** 。请使用 **[原地](http://baike.baidu.com/item/原地算法)** 算法**。**

#### 解答

```java
class Solution {
    public void setZeroes(int[][] matrix) {
        int row = matrix.length;
        int col = matrix[0].length;
        boolean row0_flag = false;
        boolean col0_flag = false;
        // 第一行是否有零
        for (int j = 0; j < col; j++) {
            if (matrix[0][j] == 0) {
                row0_flag = true;
                break;
            }
        }
        // 第一列是否有零
        for (int i = 0; i < row; i++) {
            if (matrix[i][0] == 0) {
                col0_flag = true;
                break;
            }
        }
        // 把第一行第一列作为标志位
        for (int i = 1; i < row; i++) {
            for (int j = 1; j < col; j++) {
                if (matrix[i][j] == 0) {
                    matrix[i][0] = matrix[0][j] = 0;
                }
            }
        }
        // 置0
        for (int i = 1; i < row; i++) {
            for (int j = 1; j < col; j++) {
                if (matrix[i][0] == 0 || matrix[0][j] == 0) {
                    matrix[i][j] = 0;
                }
            }
        }
        if (row0_flag) {
            for (int j = 0; j < col; j++) {
                matrix[0][j] = 0;
            }
        }
        if (col0_flag) {
            for (int i = 0; i < row; i++) {
                matrix[i][0] = 0;
            }
        } 
    }
}
```



## 滑动窗口

### 重复的DNA序列

#### 题目

**DNA序列** 由一系列核苷酸组成，缩写为 `'A'`, `'C'`, `'G'` 和 `'T'`.。

- 例如，`"ACGAATTCCG"` 是一个 **DNA序列** 。

在研究 **DNA** 时，识别 DNA 中的重复序列非常有用。

给定一个表示 **DNA序列** 的字符串 `s` ，返回所有在 DNA 分子中出现不止一次的 **长度为 `10`** 的序列(子字符串)。你可以按 **任意顺序** 返回答案。

 

**示例 1：**

```
输入：s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
输出：["AAAAACCCCC","CCCCCAAAAA"]
```

#### 解答

```java
class Solution {
    static final int L = 10;
    Map<Character, Integer> bin = new HashMap<Character, Integer>() {{
        put('A', 0);
        put('C', 1);
        put('G', 2);
        put('T', 3);
    }};

    public List<String> findRepeatedDnaSequences(String s) {
        List<String> ans = new ArrayList<String>();
        int n = s.length();
        if (n <= L) {
            return ans;
        }
        int x = 0;
        for (int i = 0; i < L - 1; ++i) {
            x = (x << 2) | bin.get(s.charAt(i));
        }
        Map<Integer, Integer> cnt = new HashMap<Integer, Integer>();
        for (int i = 0; i <= n - L; ++i) {
            x = ((x << 2) | bin.get(s.charAt(i + L - 1))) & ((1 << (L * 2)) - 1);
            cnt.put(x, cnt.getOrDefault(x, 0) + 1);
            if (cnt.get(x) == 2) {
                ans.add(s.substring(i, i + L));
            }
        }
        return ans;
    }
}
```



### 存在重复元素2

#### 题目

给你一个整数数组 `nums` 和一个整数 `k` ，判断数组中是否存在两个 **不同的索引** `i` 和 `j` ，满足 `nums[i] == nums[j]` 且 `abs(i - j) <= k` 。如果存在，返回 `true` ；否则，返回 `false` 。

 

**示例 1：**

```
输入：nums = [1,2,3,1], k = 3
输出：true
```

**示例 2：**

```
输入：nums = [1,0,1,1], k = 1
输出：true
```

#### 解答

```java
class Solution {
    public boolean containsNearbyDuplicate(int[] nums, int k) {
        Set<Integer> st=new HashSet<>();
        int len=nums.length;
        k=k+1;
        if(k>=len){
            for(int i=0;i<len;i++){
                if(st.contains(nums[i])){
                    return true;
                }
                st.add(nums[i]);
            }
        }else{
            for(int i=0;i<k;i++){
                if(st.contains(nums[i])){
                    return true;
                }
                st.add(nums[i]);
            }
            for(int i=k;i<len;i++){
                st.remove(nums[i-k]);
                if(st.contains(nums[i])){
                    return true;
                }
                st.add(nums[i]);
            }
        }
        return false;
    }
}
```





### 滑动窗口中位数

#### 题目

中位数是有序序列最中间的那个数。如果序列的长度是偶数，则没有最中间的数；此时中位数是最中间的两个数的平均数。

例如：

- `[2,3,4]`，中位数是 `3`
- `[2,3]`，中位数是 `(2 + 3) / 2 = 2.5`

给你一个数组 *nums*，有一个长度为 *k* 的窗口从最左端滑动到最右端。窗口中有 *k* 个数，每次窗口向右移动 *1* 位。你的任务是找出每次窗口移动后得到的新窗口中元素的中位数，并输出由它们组成的数组。



#### 解答

```java
class Solution {
    public double[] medianSlidingWindow(int[] nums, int k) {
        double[] rst = new double[nums.length-k+1];
        PriorityQueue<Integer> big = new PriorityQueue<>();
        PriorityQueue<Integer> small = new PriorityQueue<>(new Comparator<Integer>(){
            @Override
            public int compare(Integer a, Integer b){
                return Integer.compare(b, a);
            }
        });
        HashMap<Integer, Integer> debt = new HashMap<>();

        //balance记录了小值堆和大值堆之间数字的差值
        int i=0, j=k-1, index=0, balance=0;
        //init
        int[] tmpArray = Arrays.copyOfRange(nums, 0, k);
        Arrays.sort(tmpArray);
        int scope = (k&1)==1?k/2:k/2-1;
        for(int m=0; m<=scope; m++)
            small.offer(tmpArray[m]);
        for(int m=scope+1; m<k; m++)
            big.offer(tmpArray[m]);
        rst[index++] = insertRst(small, big, k);
        while(++j < nums.length){
            balance += deleteElment(debt, nums, i++, small, big);
            balance += insertElment(nums, j, small, big);
            makeBalance(debt, small, big, balance);
            rst[index++] = insertRst(small, big, k);
            balance = 0;
        }
        return rst;
    }

    private int deleteElment(HashMap<Integer, Integer> debt, int[] nums, int i, PriorityQueue<Integer> small, PriorityQueue<Integer> big)
    {
        int cur = nums[i];
        debt.put(cur, debt.getOrDefault(cur, 0)+1);
        return !small.isEmpty()&&nums[i]<=small.peek()?-1:1;
    }

    private int insertElment(int[] nums, int j, PriorityQueue<Integer> small, PriorityQueue<Integer> big)
    {
        if(!small.isEmpty() && nums[j]<=small.peek()){
            small.add(nums[j]);
            return 1;
        }
        big.add(nums[j]);
        return -1;
    }

    //balance记录了此时两个堆不平等的情况，需要将其平衡到初始水平，此时如果是正的，就从小堆中删除，加到大堆里，如果是负的，就反过来，平衡完之后，只需要对欠债元素进行删除就可。欠债元素必须先从small里进行删除，因为添加的时候也是优先添加到small，优先删除big中的元素极有可能导致big为空，从而导致添加中位数时出问题
    private void makeBalance(HashMap<Integer, Integer> debt, PriorityQueue<Integer> small, PriorityQueue<Integer> big, int balance)
    {
        assert balance==2||balance==-2||balance==0;
        if(balance>0)
            big.offer(small.poll());
        else if(balance<0)
            small.offer(big.poll());
        while(!small.isEmpty()&&debt.getOrDefault(small.peek(), 0) > 0){
            debt.put(small.peek(), debt.get(small.peek())-1);
            small.poll();
        }
        while(!big.isEmpty()&&debt.getOrDefault(big.peek(), 0) > 0){
            debt.put(big.peek(), debt.get(big.peek())-1);
            big.poll();
        }
    }

    private double insertRst(PriorityQueue<Integer> small, PriorityQueue<Integer> big, int k){
        return (k&1)==1?(double)small.peek():((double)small.peek()+(double)big.peek())/2;
    }
}
```

