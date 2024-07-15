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

