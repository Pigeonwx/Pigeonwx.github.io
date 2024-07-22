# 博弈算法

## 引言

博弈算法在算法题中通常用于解决竞争性问题，即两个或更多玩家在有限的资源和规则下进行决策，以最大化各自的收益。这类算法经常出现在涉及策略和对抗的题目中。常见的博弈算法有以下几种：

1. **极大极小算法（Minimax Algorithm）**：
   - 该算法用于零和博弈（即一个玩家的得分增加，另一个玩家的得分就会减少）。
   - 基本思路是模拟所有可能的对手反应，选择对自己最有利的策略。
   - 树形结构表示游戏的所有可能状态，每个节点代表一个游戏状态。
   - 叶节点的值表示该状态对当前玩家的收益。
   - 递归地选择当前玩家得分最大的路径（极大化）和对手得分最小的路径（极小化），最终找到最优策略。

2. **Alpha-Beta剪枝（Alpha-Beta Pruning）**：
   - 是对极大极小算法的优化。
   - 通过剪枝减少需要评估的节点数，提高搜索效率。
   - Alpha值表示当前玩家在某节点能够保证的最小值，Beta值表示对手在某节点能够保证的最大值。
   - 如果发现某一节点的值不能使当前路径的值更优，则该节点及其子节点可以被剪枝。

3. **博弈树搜索（Game Tree Search）**：
   - 该算法通过构建和搜索博弈树来解决问题。
   - 包括深度优先搜索（DFS）、广度优先搜索（BFS）等。
   - 搜索过程中会结合启发式函数来评估当前状态的优劣。

4. **蒙特卡罗树搜索（Monte Carlo Tree Search, MCTS）**：
   - 是一种通过随机模拟游戏进行决策的算法。
   - 包含四个步骤：选择（Selection）、扩展（Expansion）、模拟（Simulation）和回溯（Backpropagation）。
   - 选择阶段选择当前最优节点进行扩展；扩展阶段在该节点下增加新节点；模拟阶段通过随机模拟游戏结束；回溯阶段根据模拟结果更新节点值。
   - 适用于复杂的博弈问题，如围棋、国际象棋等。

5. **NegaMax算法**：
   - 是极大极小算法的简化版本。
   - 基于对称性，假设两个玩家得分相反，将问题转化为单一玩家的最大化问题。
   - 递归地对当前局面进行评估，选择使当前玩家得分最大的路径。

这些博弈算法在算法题中应用广泛，常见题型包括井字棋、国际象棋、围棋、跳棋等。掌握这些算法的基本原理和实现方法，对于解决复杂的对抗性问题非常有帮助。



## 算法题

### [292. Nim 游戏](https://leetcode.cn/problems/nim-game/)

你和你的朋友，两个人一起玩 [Nim 游戏](https://baike.baidu.com/item/Nim游戏/6737105)：

- 桌子上有一堆石头。
- 你们轮流进行自己的回合， **你作为先手** 。
- 每一回合，轮到的人拿掉 1 - 3 块石头。
- 拿掉最后一块石头的人就是获胜者。

假设你们每一步都是最优解。请编写一个函数，来判断你是否可以在给定石头数量为 `n` 的情况下赢得游戏。如果可以赢，返回 `true`；否则，返回 `false` 。

这个题目是一个典型的博弈问题。我们可以通过数学推理来解决这个问题，而不需要复杂的博弈算法。下面是解析和实现过程：

```
在 Nim 游戏中，两人轮流从一堆石头中拿走 1 到 3 块石头，拿到最后一块石头的人获胜。要判断是否能赢，我们需要分析在给定的石头数量 n 下，先手是否有必胜策略。

1. 如果石头的数量 \( n \) 是 1 到 3，先手可以一次拿完，必胜。
2. 如果石头的数量 \( n \) 是 4，无论先手拿 1、2 还是 3 块，剩下的石头都在 1 到 3 之间，后手可以拿完，先手必败。
3. 如果石头的数量 \( n \) 是 5 到 7，先手可以调整拿的石头数量，使得剩下的石头是 4 块，后手必败，所以先手必胜。
4. 如果石头的数量 \( n \) 是 8，无论先手拿 1、2 还是 3 块，剩下的石头都在 5 到 7 之间，后手可以调整拿的石头数量，使得剩下的石头是 4 块，先手必败。

通过以上分析，可以看出一个规律：

- 如果 \( n \% 4 == 0 \)，先手必败（因为后手总能使石头数量回到 4 的倍数）。
- 如果 \( n \% 4 \neq 0 \)，先手可以通过调整拿的石头数量，使得每轮后手面对的石头数量是 4 的倍数，先手必胜。
```

### [1561. 你可以获得的最大硬币数目](https://leetcode.cn/problems/maximum-number-of-coins-you-can-get/)

有 3n 堆数目不一的硬币，你和你的朋友们打算按以下方式分硬币：

- 每一轮中，你将会选出 **任意** 3 堆硬币（不一定连续）。
- Alice 将会取走硬币数量最多的那一堆。
- 你将会取走硬币数量第二多的那一堆。
- Bob 将会取走最后一堆。
- 重复这个过程，直到没有更多硬币。

给你一个整数数组 `piles` ，其中 `piles[i]` 是第 `i` 堆中硬币的数目。

返回你可以获得的最大硬币数目。

```java
class Solution {
    public int maxCoins(int[] piles) {
        Arrays.sort(piles);
        int len=piles.length;
        int sum=0;
        for(int i=1;i<=len/3;i++){
            sum+=piles[len-i*2];
        }
        return sum;
    }
}
```

### [1025. 除数博弈](https://leetcode.cn/problems/divisor-game/)

爱丽丝和鲍勃一起玩游戏，他们轮流行动。爱丽丝先手开局。

最初，黑板上有一个数字 `n` 。在每个玩家的回合，玩家需要执行以下操作：

- 选出任一 `x`，满足 `0 < x < n` 且 `n % x == 0` 。
- 用 `n - x` 替换黑板上的数字 `n` 。

如果玩家无法执行这些操作，就会输掉游戏。

*只有在爱丽丝在游戏中取得胜利时才返回 `true` 。假设两个玩家都以最佳状态参与游戏。*

```java
class Solution {
    public boolean divisorGame(int n) {
        return n%2==0;
    }
}
//数学归纳法
```

### [2038. 如果相邻两个颜色均相同则删除当前颜色](https://leetcode.cn/problems/remove-colored-pieces-if-both-neighbors-are-the-same-color/)

总共有 `n` 个颜色片段排成一列，每个颜色片段要么是 `'A'` 要么是 `'B'` 。给你一个长度为 `n` 的字符串 `colors` ，其中 `colors[i]` 表示第 `i` 个颜色片段的颜色。

Alice 和 Bob 在玩一个游戏，他们 **轮流** 从这个字符串中删除颜色。Alice **先手** 。

- 如果一个颜色片段为 `'A'` 且 **相邻两个颜色** 都是颜色 `'A'` ，那么 Alice 可以删除该颜色片段。Alice **不可以** 删除任何颜色 `'B'` 片段。
- 如果一个颜色片段为 `'B'` 且 **相邻两个颜色** 都是颜色 `'B'` ，那么 Bob 可以删除该颜色片段。Bob **不可以** 删除任何颜色 `'A'` 片段。
- Alice 和 Bob **不能** 从字符串两端删除颜色片段。
- 如果其中一人无法继续操作，则该玩家 **输** 掉游戏且另一玩家 **获胜** 。

假设 Alice 和 Bob 都采用最优策略，如果 Alice 获胜，请返回 `true`，否则 Bob 获胜，返回 `false`。

```java
class Solution {
    public boolean winnerOfGame(String colors) {
        int cnta=0;
        int cntb=0;
        int len=colors.length();
        for(int i=0;i<len;){
            char t=colors.charAt(i);
            int j=i+1;
            while(j<len&&colors.charAt(j)==t){
                j++;
            }
            if(j-i>=3){
                if(t=='A'){
                    cnta+=j-i-2;
                }else{
                    cntb+=j-i-2;
                }
            }
            i=j;
        }
        return cnta>cntb;
    }
}
```



### [877. 石子游戏](https://leetcode.cn/problems/stone-game/)

Alice 和 Bob 用几堆石子在做游戏。一共有偶数堆石子，**排成一行**；每堆都有 **正** 整数颗石子，数目为 `piles[i]` 。

游戏以谁手中的石子最多来决出胜负。石子的 **总数** 是 **奇数** ，所以没有平局。

Alice 和 Bob 轮流进行，**Alice 先开始** 。 每回合，玩家从行的 **开始** 或 **结束** 处取走整堆石头。 这种情况一直持续到没有更多的石子堆为止，此时手中 **石子最多** 的玩家 **获胜** 。

假设 Alice 和 Bob 都发挥出最佳水平，当 Alice 赢得比赛时返回 `true` ，当 Bob 赢得比赛时返回 `false` 。



```
事实上，这还是一道很经典的博弈论问题，也是最简单的一类博弈论问题。

为了方便，我们称「石子序列」为石子在原排序中的编号，下标从 1 开始。

由于石子的堆数为偶数，且只能从两端取石子。因此先手后手所能选择的石子序列，完全取决于先手每一次决定。

证明如下：

由于石子的堆数为偶数，对于先手而言：每一次的决策局面，都能「自由地」选择奇数还是偶数的序列，从而限制后手下一次「只能」奇数还是偶数石子。

具体的，对于本题，由于石子堆数为偶数，因此先手的最开始局面必然是 [奇数,偶数]，即必然是「奇偶性不同的局面」；当先手决策完之后，交到给后手的要么是 [奇数,奇数] 或者 [偶数,偶数]，即必然是「奇偶性相同的局面」；后手决策完后，又恢复「奇偶性不同的局面」交回到先手 ...

不难归纳推理，这个边界是可以应用到每一个回合。

因此先手只需要在进行第一次操作前计算原序列中「奇数总和」和「偶数总和」哪个大，然后每一次决策都「限制」对方只能选择「最优奇偶性序列」的对立面即可。

同时又由于所有石子总和为奇数，堆数为偶数，即没有平局，所以先手必胜。
```



### [1510. 石子游戏 IV](https://leetcode.cn/problems/stone-game-iv/)

Alice 和 Bob 两个人轮流玩一个游戏，Alice 先手。

一开始，有 `n` 个石子堆在一起。每个人轮流操作，正在操作的玩家可以从石子堆里拿走 **任意** 非零 **平方数** 个石子。

如果石子堆里没有石子了，则无法操作的玩家输掉游戏。

给你正整数 `n` ，且已知两个人都采取最优策略。如果 Alice 会赢得比赛，那么返回 `True` ，否则返回 `False` 。



```
根据游戏规则，每一轮都会将石子数量减少。当没有剩余的石子时，玩家无法执行操作。当还有剩余的石子时，玩家可以执行操作。

可以使用动态规划计算结果。创建长度为 n+1 的数组 dp，其中 dp[i] 为剩余 i 个石子时当前玩家的游戏结果，true 表示当前玩家获胜，false 表示当前玩家失败。

当 i=0 时，轮到的玩家无法执行操作而输掉游戏，因此动态规划的边界情况是 dp[0]=false。

当 i>0 时，当前玩家可以选择任意不超过 i 的完全平方数 j，取走 j 个石子，剩余 i−j 个石子。如果存在一个不超过 i 的完全平方数 j 满足 dp[i−j]=false，则当前玩家可以取走 j 个石子使对方玩家失败，因此当前玩家获胜；如果所有不超过 i 的完全平方数 j 都满足 dp[i−j]=true，则当前玩家失败。

因此动态规划的状态转移方程是：如果存在一个不超过 i 的完全平方数 j 满足 dp[i−j]=false，则 dp[i]=true；如果所有不超过 i 的完全平方数 j 都满足 dp[i−j]=true，则 dp[i]=false。

根据动态规划的状态转移方程，计算 dp[i] 的顺序为从到大小遍历每个 i。计算得到 dp[n] 即为游戏结果。
```

```java
class Solution {
    public boolean winnerSquareGame(int n) {
        boolean[] dp = new boolean[n + 1];
        for (int i = 1; i <= n; i++) {
            boolean flag = false;
            for (int j = 1; j * j <= i && !flag; j++) {
                if (!dp[i - j * j]) {
                    flag = true;
                }
            }
            dp[i] = flag;
        }
        return dp[n];
    }
}
```



### [486. 预测赢家](https://leetcode.cn/problems/predict-the-winner/)

给你一个整数数组 `nums` 。玩家 1 和玩家 2 基于这个数组设计了一个游戏。

玩家 1 和玩家 2 轮流进行自己的回合，玩家 1 先手。开始时，两个玩家的初始分值都是 `0` 。每一回合，玩家从数组的任意一端取一个数字（即，`nums[0]` 或 `nums[nums.length - 1]`），取到的数字将会从数组中移除（数组长度减 `1` ）。玩家选中的数字将会加到他的得分上。当数组中没有剩余数字可取时，游戏结束。

如果玩家 1 能成为赢家，返回 `true` 。如果两个玩家得分相等，同样认为玩家 1 是游戏的赢家，也返回 `true` 。你可以假设每个玩家的玩法都会使他的分数最大化。

```java
class Solution {
    public boolean predictTheWinner(int[] nums) {
        int len=nums.length;
        int[][] dp=new int[len+2][len+2];
        for(int l=1;l<=len;l++){
            for(int i=1;i<=len&&i+l-1<=len;i++){
                int j=i+l-1;
                dp[i][j]=Math.max(nums[i-1]-dp[i+1][j],nums[j-1]-dp[i][j-1]);
            }
        }
        return dp[1][len]>=0;
    }
}
```



### [1686. 石子游戏 VI](https://leetcode.cn/problems/stone-game-vi/)

Alice 和 Bob 轮流玩一个游戏，Alice 先手。

一堆石子里总共有 `n` 个石子，轮到某个玩家时，他可以 **移出** 一个石子并得到这个石子的价值。Alice 和 Bob 对石子价值有 **不一样的的评判标准** 。双方都知道对方的评判标准。

给你两个长度为 `n` 的整数数组 `aliceValues` 和 `bobValues` 。`aliceValues[i]` 和 `bobValues[i]` 分别表示 Alice 和 Bob 认为第 `i` 个石子的价值。

所有石子都被取完后，得分较高的人为胜者。如果两个玩家得分相同，那么为平局。两位玩家都会采用 **最优策略** 进行游戏。

请你推断游戏的结果，用如下的方式表示：

- 如果 Alice 赢，返回 `1` 。
- 如果 Bob 赢，返回 `-1` 。
- 如果游戏平局，返回 `0` 。



```java
class Solution {
    public int stoneGameVI(int[] a, int[] b) {
        int n = a.length;
        Integer[] ids = new Integer[n];
        for (int i = 0; i < n; i++) {
            ids[i] = i;
        }
        Arrays.sort(ids, (i, j) -> a[j] + b[j] - a[i] - b[i]);
        int diff = 0;
        for (int i = 0; i < n; i++) {
            diff += i % 2 == 0 ? a[ids[i]] : -b[ids[i]];
        }
        return Integer.compare(diff, 0);
    }
}
```



### [1690. 石子游戏 VII](https://leetcode.cn/problems/stone-game-vii/)

石子游戏中，爱丽丝和鲍勃轮流进行自己的回合，**爱丽丝先开始** 。

有 `n` 块石子排成一排。每个玩家的回合中，可以从行中 **移除** 最左边的石头或最右边的石头，并获得与该行中剩余石头值之 **和** 相等的得分。当没有石头可移除时，得分较高者获胜。

鲍勃发现他总是输掉游戏（可怜的鲍勃，他总是输），所以他决定尽力 **减小得分的差值** 。爱丽丝的目标是最大限度地 **扩大得分的差值** 。

给你一个整数数组 `stones` ，其中 `stones[i]` 表示 **从左边开始** 的第 `i` 个石头的值，如果爱丽丝和鲍勃都 **发挥出最佳水平** ，请返回他们 **得分的差值** 。

```java
class Solution {
    public int stoneGameVII(int[] stones) {
        int len=stones.length;
        int []sum=new int[len+1];
        for (int i = 0; i < len; i++) {
            sum[i + 1] += sum[i] + stones[i];
        }
        int[][] dp=new int[len+2][len+2];
        for(int l=1;l<=len;l++){
            for(int i=1;i<=len&&i+l-1<=len;i++){
                int j=i+l-1;
                dp[i][j]=Math.max(sum[j]-sum[i]-dp[i+1][j],sum[j-1]-sum[i-1]-dp[i][j-1]);
            }
        }
        return dp[1][len];
    }
}
```



### [1140. 石子游戏 II](https://leetcode.cn/problems/stone-game-ii/)

爱丽丝和鲍勃继续他们的石子游戏。许多堆石子 **排成一行**，每堆都有正整数颗石子 `piles[i]`。游戏以谁手中的石子最多来决出胜负。

爱丽丝和鲍勃轮流进行，爱丽丝先开始。最初，`M = 1`。

在每个玩家的回合中，该玩家可以拿走剩下的 **前** `X` 堆的所有石子，其中 `1 <= X <= 2M`。然后，令 `M = max(M, X)`。

游戏一直持续到所有石子都被拿走。

假设爱丽丝和鲍勃都发挥出最佳水平，返回爱丽丝可以得到的最大数量的石头。

```java
class Solution {
    public int stoneGameII(int[] piles) {
        int s = 0, n = piles.length;
        int[][] f = new int[n][n + 1];
        for (int i = n - 1; i >= 0; --i) {
            s += piles[i];
            for (int m = 1; m <= i / 2 + 1; ++m) {
                if (i + m * 2 >= n) f[i][m] = s; // 全拿
                else {
                    int mn = Integer.MAX_VALUE;
                    for (int x = 1; x <= m * 2; ++x)
                        mn = Math.min(mn, f[i + x][Math.max(m, x)]);
                    f[i][m] = s - mn;
                }
            }
        }
        return f[0][1];
    }
}
```



### [1927. 求和游戏](https://leetcode.cn/problems/sum-game/)

Alice 和 Bob 玩一个游戏，两人轮流行动，**Alice 先手** 。

给你一个 **偶数长度** 的字符串 `num` ，每一个字符为数字字符或者 `'?'` 。每一次操作中，如果 `num` 中至少有一个 `'?'` ，那么玩家可以执行以下操作：

1. 选择一个下标 `i` 满足 `num[i] == '?'` 。
2. 将 `num[i]` 用 `'0'` 到 `'9'` 之间的一个数字字符替代。

当 `num` 中没有 `'?'` 时，游戏结束。

Bob 获胜的条件是 `num` 中前一半数字的和 **等于** 后一半数字的和。Alice 获胜的条件是前一半的和与后一半的和 **不相等** 。

- 比方说，游戏结束时 `num = "243801"` ，那么 Bob 获胜，因为 `2+4+3 = 8+0+1` 。如果游戏结束时 `num = "243803"` ，那么 Alice 获胜，因为 `2+4+3 != 8+0+3` 。

在 Alice 和 Bob 都采取 **最优** 策略的前提下，如果 Alice 获胜，请返回 `true` ，如果 Bob 获胜，请返回 `false` 。



![截屏2024-07-15-22.31.24](/Users/xiangjianhang/pigeonwx.github.io/docs/算法/game/截屏2024-07-15-22.31.24.png)

![截屏2024-07-15-22.32.12](/Users/xiangjianhang/pigeonwx.github.io/docs/算法/game/截屏2024-07-15-22.32.12.png)

```c++
class Solution {
public:
    bool sumGame(string num) {
        int n = num.size(), sum1 = 0, cnt1 = 0, sum2 = 0, cnt2 = 0;
        for(int i = 0; i < n / 2; ++i) 
            sum1 += (num[i] == '?' ? 0 : (num[i] - '0')), cnt1 += (num[i] == '?');
        for(int i = n / 2; i < n; ++i) 
            sum2 += (num[i] == '?' ? 0 : (num[i] - '0')), cnt2 += (num[i] == '?');
        if((cnt1 + cnt2) & 1) return true;
        return 9 * (cnt1 - cnt2) / 2 + sum1 - sum2 != 0;
    }
};
```



### [1406. 石子游戏 III](https://leetcode.cn/problems/stone-game-iii/)

Alice 和 Bob 继续他们的石子游戏。几堆石子 **排成一行** ，每堆石子都对应一个得分，由数组 `stoneValue` 给出。

Alice 和 Bob 轮流取石子，**Alice** 总是先开始。在每个玩家的回合中，该玩家可以拿走剩下石子中的的前 **1、2 或 3 堆石子** 。比赛一直持续到所有石头都被拿走。

每个玩家的最终得分为他所拿到的每堆石子的对应得分之和。每个玩家的初始分数都是 **0** 。

比赛的目标是决出最高分，得分最高的选手将会赢得比赛，比赛也可能会出现平局。

假设 Alice 和 Bob 都采取 **最优策略** 。

如果 Alice 赢了就返回 `"Alice"` *，*Bob 赢了就返回 `"Bob"`*，*分数相同返回 `"Tie"` 。

```java
class Solution {
    public String stoneGameIII(int[] stoneValue) {
        int n = stoneValue.length;
        int[] suffixSum = new int[n];
        suffixSum[n - 1] = stoneValue[n - 1];
        for (int i = n - 2; i >= 0; --i) {
            suffixSum[i] = suffixSum[i + 1] + stoneValue[i];
        }
        int[] f = new int[n + 1];
        // 边界情况，当没有石子时，分数为 0
        // 为了代码的可读性，显式声明
        f[n] = 0;
        for (int i = n - 1; i >= 0; --i) {
            int bestj = f[i + 1];
            for (int j = i + 2; j <= i + 3 && j <= n; ++j) {
                bestj = Math.min(bestj, f[j]);
            }
            f[i] = suffixSum[i] - bestj;
        }
        int total = 0;
        for (int value : stoneValue) {
            total += value;
        }
        if (f[0] * 2 == total) {
            return "Tie";
        } else {
            return f[0] * 2 > total ? "Alice" : "Bob";
        }
    }
}
```



### [464. 我能赢吗](https://leetcode.cn/problems/can-i-win/)

在 "100 game" 这个游戏中，两名玩家轮流选择从 `1` 到 `10` 的任意整数，累计整数和，先使得累计整数和 **达到或超过** 100 的玩家，即为胜者。

如果我们将游戏规则改为 “玩家 **不能** 重复使用整数” 呢？例如，两个玩家可以轮流从公共整数池中抽取从 1 到 15 的整数（不放回），直到累计整数和 >= 100。

给定两个整数 `maxChoosableInteger` （整数池中可选择的最大数）和 `desiredTotal`（累计和），若先出手的玩家能稳赢则返回 `true` ，否则返回 `false` 。假设两位玩家游戏时都表现 **最佳** 。

```java
class Solution {
    int n, t;
    int[] f = new int[1 << 20];
    // 1 true / -1 false
    int dfs(int state, int tot) {
        if (f[state] != 0) return f[state];
        for (int i = 0; i < n; i++) {
            if (((state >> i) & 1) == 1) continue;
            if (tot + i + 1 >= t) return f[state] = 1;
            if (dfs(state | (1 << i), tot + i + 1) == -1) return f[state] = 1;
        }
        return f[state] = -1;
    }
    public boolean canIWin(int _n, int _t) {
        n = _n; t = _t;
        if (n * (n + 1) / 2 < t) return false;
        if (t == 0) return true;
        return dfs(0, 0) == 1;
    }
}
```



### [2029. 石子游戏 IX](https://leetcode.cn/problems/stone-game-ix/)

Alice 和 Bob 再次设计了一款新的石子游戏。现有一行 n 个石子，每个石子都有一个关联的数字表示它的价值。给你一个整数数组 `stones` ，其中 `stones[i]` 是第 `i` 个石子的价值。

Alice 和 Bob 轮流进行自己的回合，**Alice** 先手。每一回合，玩家需要从 `stones` 中移除任一石子。

- 如果玩家移除石子后，导致 **所有已移除石子** 的价值 **总和** 可以被 3 整除，那么该玩家就 **输掉游戏** 。
- 如果不满足上一条，且移除后没有任何剩余的石子，那么 Bob 将会直接获胜（即便是在 Alice 的回合）。

假设两位玩家均采用 **最佳** 决策。如果 Alice 获胜，返回 `true` ；如果 Bob 获胜，返回 `false` 。

 

**示例 1：**

```
输入：stones = [2,1]
输出：true
解释：游戏进行如下：
- 回合 1：Alice 可以移除任意一个石子。
- 回合 2：Bob 移除剩下的石子。 
已移除的石子的值总和为 1 + 2 = 3 且可以被 3 整除。因此，Bob 输，Alice 获胜。
```



为了方便，我们用 A 来代指 Alice，用 B 带代指 Bob。A 只有一种获胜方式，是使得 B 在选石子时凑成 3 的倍数；而 B 除了能够通过让 A 凑成 3 的倍数以外，还能通过让游戏常规结束来获胜。

因此整个游戏过程，我们只需要关心「已被移除的石子总和」和「剩余石子个数/价值情况」即可。更进一步的，我们只需关心已被移除的石子总和是否为 3 的倍数，以及剩余石子的价值与已移除石子总和相加是否凑成 3 的倍数即可。所以我们可以按照石子价值除以 3 的余数分成三类，并统计相应数量。不失一般性考虑，某个回合开始前，已移除的石子总和状态为 x（共三种，分别为除以 3 余数为 0、1 和 2，其中当状态为 0，且非首个回合时，说明凑成 3 的倍数，游戏结束），剩余石子价值除以 3 的余数 s 分别为 0、1 和 2。

首先如果当前 x=1 时，不能选择 s=2 的石子，否则会导致凑成总和为 3 的倍数而失败；同理 x=2 时，不能选择 s=1 的石子；而选择 s=0 的数字，不会改变 x 的状态，可看做换手操作。同时成对的 s=0 的等价于没有 s=0 的石子（双方只需要轮流选完这些 s=0 的石子，最终会回到先手最开始的局面）；而选择与 x 相同的 s 会导致 x 改变（即 x=1 时，选择 s=1 的石子，会导致 x=2；而 x=2 时，选 s=2 的石子，会导致 x=1）。明确规则后，是分情况讨论的过程：



- s=0 的石子数量为偶数：此时等价于没有 s=0 的石子，我们只需要关心 s=1 和 s=2 即可：
  - s=1 的石子数量为 0： 这意味着 A 开始选择的只能是 s=2，此时交给 B 的局面为「x=2、剩余石子只有 s=2」，此时 B 只能选 s=2 的石子，由于 x=2 且选择的石子 s=2，因此交由回 A 的局面为「x=1，剩余是在只有 s=2」，因此游戏继续的话 A 必败，同时如果在该过程的任何时刻石子被取完，也是 B 直接获胜，即 A 仍为必败；
  - s=2 的石子数量为 0：分析同理，A 只能选 s=1，此时交给 B 的局面为「x=1、剩余石子只有 s=1」，此时 B 只能选 s=1 的石子，由于 x=1 且选择的石子 s=1，因此交由回 A 的局面为「x=2，剩余是在只有 s=1」，因此游戏继续的话 A 必败，同时如果在该过程的任何时刻石子被取完，也是 B 直接获胜，即 A 仍为必败；
  - s=1 和 s=2 的石子数量均不为 0：A 选数量不是最多的一类石子，B 下一回合只能选择相同类型的石子（或是无从选择导致失败），然后游戏继续，最终 B 会先进入「只能凑成 3 的倍数」的局面导致失败，即 A 必胜。

- s=0 的石子数量为奇数：此时等价于有一次换手机会，该换手机会必然应用在「对必败局面进行转移」才有意义，因此只有 s=1 和 s=2 的石子数量差大于 2，A 的先手优势不会因为存在换手机会而被转移：
  - 两者数量差不超过 2：此时 B 可以利用「对方凑成 3 的倍数必败」规则和「优先使用 s=0 石子」权利来进入确保自己为必胜态：
    - 举个 🌰，当 s=1 和 s=2 的石子数量相等，虽然有 s=0 的石子，A 先手，但是 A 的首个回合必然不能选 s=0，否则马上失败结束，因此 A 只能选 s=1 或 s=2，此时 B直接选择 s=0 的石子，交由给 A 的局面 x 没有发生改变，A 只能选择与首个回合相同的 s 游戏才能继续，因此局面会变为「B 先手、s=1 和 s=2 的石子数量差为 2」，游戏继续，最终 A 会先遇到「只能凑成 3 的倍数」的局面，即 B 必胜。
    - 两者数量不等，但数量差不超过 2：此时无论 A 选择数量较少或较多的 s，B 都在第二回合马上使用 s=0 的石子进行换手，A 只能继续选与第一回合相同类型的的石子，游戏才能进行，最终 A 会先遇到「只能凑成 3 的倍数」或「石子被取完」的局面，即 B 必胜。
  - 两者数量差超过 2 ：此时即使 A 只要确保第一次选择数量较多的 s，不管 B 是否使用「优先使用 s=0」的石子，A 都有足够次数数量多 s 来抵消换手（或是在 B 放弃使用 s=0 之后马上使用），最终都是 B 最先遇到「只能凑成 3 的倍数」的局面，即 A 获胜。





### [810. 黑板异或游戏](https://leetcode.cn/problems/chalkboard-xor-game/)

黑板上写着一个非负整数数组 `nums[i]` 。

Alice 和 Bob 轮流从黑板上擦掉一个数字，Alice 先手。如果擦除一个数字后，剩余的所有数字按位异或运算得出的结果等于 `0` 的话，当前玩家游戏失败。 另外，如果只剩一个数字，按位异或运算得到它本身；如果无数字剩余，按位异或运算结果为 `0`。

并且，轮到某个玩家时，如果当前黑板上所有数字按位异或运算结果等于 `0` ，这个玩家获胜。

假设两个玩家每步都使用最优解，当且仅当 Alice 获胜时返回 `true`。

 

**示例 1：**

```
输入: nums = [1,1,2]
输出: false
解释: 
Alice 有两个选择: 擦掉数字 1 或 2。
如果擦掉 1, 数组变成 [1, 2]。剩余数字按位异或得到 1 XOR 2 = 3。那么 Bob 可以擦掉任意数字，因为 Alice 会成为擦掉最后一个数字的人，她总是会输。
如果 Alice 擦掉 2，那么数组变成[1, 1]。剩余数字按位异或得到 1 XOR 1 = 0。Alice 仍然会输掉游戏。
```



![Snipaste_2024-07-20_11-13-03](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/算法/game/Snipaste_2024-07-20_11-13-03.png)

![Snipaste_2024-07-20_11-13-48](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/算法/game/Snipaste_2024-07-20_11-13-48.png)



### [1563. 石子游戏 V](https://leetcode.cn/problems/stone-game-v/)



几块石子 **排成一行** ，每块石子都有一个关联值，关联值为整数，由数组 `stoneValue` 给出。

游戏中的每一轮：Alice 会将这行石子分成两个 **非空行**（即，左侧行和右侧行）；Bob 负责计算每一行的值，即此行中所有石子的值的总和。Bob 会丢弃值最大的行，Alice 的得分为剩下那行的值（每轮累加）。如果两行的值相等，Bob 让 Alice 决定丢弃哪一行。下一轮从剩下的那一行开始。

只 **剩下一块石子** 时，游戏结束。Alice 的分数最初为 **`0`** 。

返回 **Alice 能够获得的最大分数** *。*

 

**示例 1：**

```
输入：stoneValue = [6,2,3,4,5,5]
输出：18
解释：在第一轮中，Alice 将行划分为 [6，2，3]，[4，5，5] 。左行的值是 11 ，右行的值是 14 。Bob 丢弃了右行，Alice 的分数现在是 11 。
在第二轮中，Alice 将行分成 [6]，[2，3] 。这一次 Bob 扔掉了左行，Alice 的分数变成了 16（11 + 5）。
最后一轮 Alice 只能将行分成 [2]，[3] 。Bob 扔掉右行，Alice 的分数现在是 18（16 + 2）。游戏结束，因为这行只剩下一块石头了。
```





![Snipaste_2024-07-20_11-27-30](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/算法/game/Snipaste_2024-07-20_11-27-30.png)

![Snipaste_2024-07-20_11-27-51](/Users/xiangjianhang/init-git/pigeonwx.github.io/docs/算法/game/Snipaste_2024-07-20_11-27-51.png)





### [1872. 石子游戏 VIII](https://leetcode.cn/problems/stone-game-viii/)

Alice 和 Bob 玩一个游戏，两人轮流操作， **Alice 先手** 。

总共有 `n` 个石子排成一行。轮到某个玩家的回合时，如果石子的数目 **大于 1** ，他将执行以下操作：

1. 选择一个整数 `x > 1` ，并且 **移除** 最左边的 `x` 个石子。
2. 将 **移除** 的石子价值之 **和** 累加到该玩家的分数中。
3. 将一个 **新的石子** 放在最左边，且新石子的值为被移除石子值之和。

当只剩下 **一个** 石子时，游戏结束。

Alice 和 Bob 的 **分数之差** 为 `(Alice 的分数 - Bob 的分数)` 。 Alice 的目标是 **最大化** 分数差，Bob 的目标是 **最小化** 分数差。

给你一个长度为 `n` 的整数数组 `stones` ，其中 `stones[i]` 是 **从左边起** 第 `i` 个石子的价值。请你返回在双方都采用 **最优** 策略的情况下，Alice 和 Bob 的 **分数之差** 。

 

**示例 1：**

```
输入：stones = [-1,2,-3,4,-5]
输出：5
解释：
- Alice 移除最左边的 4 个石子，得分增加 (-1) + 2 + (-3) + 4 = 2 ，并且将一个价值为 2 的石子放在最左边。stones = [2,-5] 。
- Bob 移除最左边的 2 个石子，得分增加 2 + (-5) = -3 ，并且将一个价值为 -3 的石子放在最左边。stones = [-3] 。
两者分数之差为 2 - (-3) = 5 。
```



```java
class Solution {
    public int stoneGameVIII(int[] stones) {
        int n = stones.length;
        int sum = 0;
        for(int i = 0; i < n; i++){
            sum += stones[i];
        }

        int res = sum;

        for(int i = n - 1; i >= 2; i--){
            sum -= stones[i];
            res = Math.max(res, sum - res);
        }
        return res;
    }
}
```





### [913. 猫和老鼠](https://leetcode.cn/problems/cat-and-mouse/)

两位玩家分别扮演猫和老鼠，在一张 **无向** 图上进行游戏，两人轮流行动。

图的形式是：`graph[a]` 是一个列表，由满足 `ab` 是图中的一条边的所有节点 `b` 组成。

老鼠从节点 `1` 开始，第一个出发；猫从节点 `2` 开始，第二个出发。在节点 `0` 处有一个洞。

在每个玩家的行动中，他们 **必须** 沿着图中与所在当前位置连通的一条边移动。例如，如果老鼠在节点 `1` ，那么它必须移动到 `graph[1]` 中的任一节点。

此外，猫无法移动到洞中（节点 `0`）。

然后，游戏在出现以下三种情形之一时结束：

- 如果猫和老鼠出现在同一个节点，猫获胜。
- 如果老鼠到达洞中，老鼠获胜。
- 如果某一位置重复出现（即，玩家的位置和移动顺序都与上一次行动相同），游戏平局。

给你一张图 `graph` ，并假设两位玩家都都以最佳状态参与游戏：

- 如果老鼠获胜，则返回 `1`；
- 如果猫获胜，则返回 `2`；
- 如果平局，则返回 `0` 。



```
class Solution {
    static int N = 55;
    static int[][][] f = new int[2 * N * N][N][N];
    int[][] g;
    int n;
    public int catMouseGame(int[][] graph) {
        g = graph;
        n = g.length;
        for (int k = 0; k < 2 * n * n; k++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    f[k][i][j] = -1;
                }
            }
        }
        return dfs(0, 1, 2);
    }
    // 0:draw / 1:mouse / 2:cat
    int dfs(int k, int a, int b) {
        int ans = f[k][a][b];
        if (a == 0) ans = 1;
        else if (a == b) ans = 2;
        else if (k >= 2 * n * n) ans = 0;
        else if (ans == -1) {
            if (k % 2 == 0) { // mouse
                boolean win = false, draw = false;
                for (int ne : g[a]) {
                    int t = dfs(k + 1, ne, b);
                    if (t == 1) win = true;
                    else if (t == 0) draw = true;
                    if (win) break;
                }
                if (win) ans = 1;
                else if (draw) ans = 0;
                else ans = 2;
            } else { // cat
                boolean win = false, draw = false;
                for (int ne : g[b]) {
                    if (ne == 0) continue;
                    int t = dfs(k + 1, a, ne);
                    if (t == 2) win = true;
                    else if (t == 0) draw = true;
                    if (win) break;
                }
                if (win) ans = 2;
                else if (draw) ans = 0;
                else ans = 1;
            }
        }
        f[k][a][b] = ans;
        return ans;
    }
}
```



### [1728. 猫和老鼠 II](https://leetcode.cn/problems/cat-and-mouse-ii/)

一只猫和一只老鼠在玩一个叫做猫和老鼠的游戏。

它们所处的环境设定是一个 `rows x cols` 的方格 `grid` ，其中每个格子可能是一堵墙、一块地板、一位玩家（猫或者老鼠）或者食物。

- 玩家由字符 `'C'` （代表猫）和 `'M'` （代表老鼠）表示。
- 地板由字符 `'.'` 表示，玩家可以通过这个格子。
- 墙用字符 `'#'` 表示，玩家不能通过这个格子。
- 食物用字符 `'F'` 表示，玩家可以通过这个格子。
- 字符 `'C'` ， `'M'` 和 `'F'` 在 `grid` 中都只会出现一次。

猫和老鼠按照如下规则移动：

- 老鼠 **先移动** ，然后两名玩家轮流移动。
- 每一次操作时，猫和老鼠可以跳到上下左右四个方向之一的格子，他们不能跳过墙也不能跳出 `grid` 。
- `catJump` 和 `mouseJump` 是猫和老鼠分别跳一次能到达的最远距离，它们也可以跳小于最大距离的长度。
- 它们可以停留在原地。
- 老鼠可以跳跃过猫的位置。

游戏有 4 种方式会结束：

- 如果猫跟老鼠处在相同的位置，那么猫获胜。
- 如果猫先到达食物，那么猫获胜。
- 如果老鼠先到达食物，那么老鼠获胜。
- 如果老鼠不能在 1000 次操作以内到达食物，那么猫获胜。

给你 `rows x cols` 的矩阵 `grid` 和两个整数 `catJump` 和 `mouseJump` ，双方都采取最优策略，如果老鼠获胜，那么请你返回 `true` ，否则返回 `false` 。



```java
import java.time.Clock;
class Solution {
    static int S = 8 * 8 * 8 * 8, K = 1000;
    static int[][] f = new int[S][K]; // mouse : 0 / cat : 1
    String[] g;
    int n, m, a, b, tx, ty;
    int[][] dirs = new int[][]{{1,0}, {-1,0}, {0,1}, {0,-1}};
    // mouse : (x, y) / cat : (p, q)
    int dfs(int x, int y, int p, int q, int k) {
        int state = (x << 9) | (y << 6) | (p << 3) | q;
        if (k == K - 1) return f[state][k] = 1;
        if (x == p && y == q) return f[state][k] = 1;
        if (x == tx && y == ty) return f[state][k] = 0;
        if (p == tx && q == ty) return f[state][k] = 1;
        if (f[state][k] != -1) return f[state][k];
        if (k % 2 == 0) { // mouse
            for (int[] di : dirs) {
                for (int i = 0; i <= b; i++) {
                    int nx = x + di[0] * i, ny = y + di[1] * i;
                    if (nx < 0 || nx >= n || ny < 0 || ny >= m) break;
                    if (g[nx].charAt(ny) == '#') break;
                    if (dfs(nx, ny, p, q, k + 1) == 0) return f[state][k] = 0;
                }
            }
            return f[state][k] = 1;
        } else { // cat
            for (int[] di : dirs) {
                for (int i = 0; i <= a; i++) {
                    int np = p + di[0] * i, nq = q + di[1] * i;
                    if (np < 0 || np >= n || nq < 0 || nq >= m) break;
                    if (g[np].charAt(nq) == '#') break;
                    if (dfs(x, y, np, nq, k + 1) == 1) return f[state][k] = 1;
                }
            }
            return f[state][k] = 0;
        }
    }
    public boolean canMouseWin(String[] grid, int catJump, int mouseJump) {
        g = grid;
        n = g.length; m = g[0].length(); a = catJump; b = mouseJump;
        for (int i = 0; i < S; i++) Arrays.fill(f[i], -1);
        int x = 0, y = 0, p = 0, q = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (g[i].charAt(j) == 'M') {
                    x = i; y = j;
                } else if (g[i].charAt(j) == 'C') {
                    p = i; q = j;
                } else if (g[i].charAt(j) == 'F') {
                    tx = i; ty = j;
                }
            }
        }
        return dfs(x, y, p, q, 0) == 0;
    }
}
```





