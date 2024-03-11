# 浙江大学机考算法

[TOC]

# 机考流程

> 复试100 = 80面试+20机考
>
> 10-20 个满分+10-20个0分
>
> 及格60 -机考 0 = 60/0.8=75（面试至少75）
>
> 总共3小时：建议第一遍过完4个题目（1小时内）  
>
> 紫金港考｜软院+计算机学院 ｜OJ = PAT + 排名 + 题目通过率
>
> 题型：30+25+25+20 ，中文，特点：应用性比较强（题目比较长，要提取关键信息）

- 小技巧1：看通过率判别哪个相对简单
- 小技巧2：测一下结果（下策）





# 一、链表





# 二、树

## 2.1 树的构造

### 2.1.1 静态实现

```c++
// 定义树节点
struct TreeNode {
    int data;
    TreeNode* left;
    TreeNode* right;
};
```

### 2.1.2 动态实现

```c++
struct TreeNode {
    int data;
    TreeNode* left;
    TreeNode* right;
};
```



## 2.2 树的遍历

### 2.2.1 基本代码

- 先序遍历
- 中序遍历
- 后序遍历
- 层序遍历

### 2.2.2 算法题目

#### 2.2.2.1 PAT A1020 



#### 2.2.2.2 PAT A1053  Path of Equal Weight



#### PAT A1043  Is it a Binary Search Tree



## 2.3 平衡二叉树

- 平衡因子

![balancetree](./zju_algo/balancetree.png)

- 左旋![左旋](./zju_algo/左旋.png)
- 右旋![右旋](./算法/zju_algo/右旋.png)

- LL ![LL](./zju_algo/LL.png)
- LR ![LR](./zju_algo/LR.png)

- RR ![RR](./zju_algo/RR.png)
- RL![RL](./zju_algo/RL.png)

### 基本代码

```c++
//
// Created by 项建航 on 2024/3/11.
//
#include "tree.h"
#include <stdio.h>
#include <math.h>
#include <algorithm>

using namespace std;
struct Node {
    int value;
    int height;//当前节点的子树高度(包括当前节点)
    Node *lchild, *rchild;
};

Node *newNode(int v) {
    Node *node = new Node;
    node->value = v;
    node->height = 1;
    node->lchild = NULL;
    node->rchild = NULL;
}

//获取以 root 为根结点的子树的当前 height
int getHeight(Node *root) {
    if (root == NULL) return 0;
    else return root->height;
}

//计算结点 root 的平衡因子
int getBalanceFactor(Node *root) {
    return getHeight(root->lchild) - getHeight(root->rchild);
}

//更新结点 root 的 height
void updateHeight(Node *root) {
    //max(左孩子的 height，右孩子的 height） + 1
    root->height = max(getHeight(root->lchild), getHeight(root->rchild)) + 1;
}

//左旋（Left Rotation)
void L(Node *&root) {
    Node *temp = root->rchild;
    root->rchild = temp->lchild;
    temp->lchild = root;
    updateHeight(root);
    updateHeight(temp);
    root = temp;
}

//右旋（Right Rotation)
void R(Node *&root) {
    Node *temp = root->lchild;
    root->lchild = temp->rchild;
    temp->rchild = root;
    updateHeight(root);
    updateHeight(temp);
    root = temp;
}

void insert(Node *&root, int v) {
    if (root == NULL) {
        root = newNode(v);
        return;
    }
    if (v < root->value) {
        insert(root->lchild, v);
        updateHeight(root);
        if (getBalanceFactor(root) == 2) {
            if (getBalanceFactor(root->lchild) == 1) { //LL型
                R(root);
            } else if (getBalanceFactor(root->lchild) == -1)
                //LR 型
                L(root->lchild);
            R(root);
        }
    } else {
        insert(root->rchild, v);
        updateHeight(root);
        if (getBalanceFactor(root) == -2) {
            if (getBalanceFactor(root->rchild) == -1) {
                //RR 型
                L(root);
            } else if (getBalanceFactor(root->rchild) == 1) {
                //RL 型
                R(root->rchild);
                L(root);
            }
        }
    }
}

//AVL 树的建立
Node *Create(int data[], int n) {
    Node *root = NULL;
    for (int i = 0; i < n; i++) {
        insert(root, data[i]); //将 data[0]~data[n-1]插入 AVL 树中
    }
    return root;
}
```



## 2.4 并查集

![zippath](./zju_algo/zippath.png)

### **基本代码**

```c++
#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <queue>
#include <sstream>

using namespace std;
const int N = 10;
int father[N];
//findFather 函数返回元素 × 所在集合的根结点
int findFather_Iter(int x) {
    while (x != father[x]) { //如果不是根结点，继续循环
        x = father[x]; //获得自己的父亲结点
    }
    return x;
}

int findFather_recur(int x) {
    if (x == father[x]) return x; //如果找到根结点，则返回根结点编号 x
    else return findFather_recur(father[x]); //否则，递归判断 x 的父亲结点是否是根结点
}

void Union(int a, int b) {
    int faA = findFather_Iter(a);//查找 a 的根结点，记为 faA
    int faB = findFather_Iter(b);//查找 b 的根结点，记为 faB
    if (faA != faB) {
        //如果不属于同一个集合
        father[faA] = faB; //合并它们
    }
}
int findFather_zip(int x){
    int f=x;
    while (f != father[f]) { //如果不是根结点，继续循环
        f = father[f]; //获得自己的父亲结点
    }
    while(x!=father[x]){
        int z=x;
        father[x]=f;
    }
    return f;
}
int main() {
    //初始化
    for (int i = 1; i <= N; i++) {
        father[i] = i; //令father[i]为-1也可,此处以father[i] = i为例
    }
    return 0;
}

```







## 2.5 堆

### 基本代码

```java
//
// Created by 项建航 on 2024/3/11.
//
#include "tree.h"
#include <stdio.h>
#include <math.h>
#include <algorithm>

using namespace std;
struct Node {
    int value;
};

const int maxn = 100;
int heap[maxn];

//最大堆
void downAdjust(int low, int high) {
    int i = low, j = i * 2;
    while (j <= high) {
        if (j + 1 <= high && heap[j + 1] > heap[j])
            j = j + 1;
        if (heap[j] > heap[i]) {
            swap(heap[j], heap[i]);
            i = j;
            j = i * 2;
        } else {
            break;
        }
    }
}

//最大堆
void upAdjust(int low, int high) {
    int i = high, j = i / 2;
    while (j >= low) {
        if (heap[j] < heap[i]) {
            swap(heap[j], heap[i]);
            i = j;
            j = i / 2;
        } else {
            break;
        }
    }
}

```

### 优先级队列实现最小堆-STL

```c++
#include <iostream>
#include <queue>
using namespace std;
struct Node{
  int x, y;
  Node( int a= 0, int b= 0 ):
  x(a), y(b) {}
};
bool operator >( Node a, Node b ){
  //返回true，a的优先级大于b
  //x大的排在队前部；x相同时，y大的排在队前部
  if( a.x== b.x ) return a.y> b.y;
  return a.x> b.x; 
}
int main(){
  priority_queue<Node,vector<Node>,greater<Node> > q;
  for( int i= 0; i< 10; ++i )
    q.push( Node( rand(), rand() ) );
  while( !q.empty() ){
    cout << q.top().x << ' ' << q.top().y << endl;
    q.pop();
  }
  return 0;
}

```



## 2.6 哈夫曼编码

### 基本代码

```c++
//
// Created by 项建航 on 2024/3/11.
//
#include "tree.h"
#include <stdio.h>
#include <math.h>
#include <algorithm>

using namespace std;

#include <queue>

using namespace std;
//代表小顶堆的优先队列
priority_queue<long long, vector<long long>, greater<long long>> q;

int main() {
    int n;
    long long temp, x, y, ans = 0;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        scanf("%lld", &temp);
    }
    q.push(temp);
    while (q.size() > 1) {
        x = q.top();
        q.pop();
        y = q.top();
        q.pop();
        q.push(x + y);
        ans += x + y;
    }
    printf("%ld\n", ans);
    return 0;
}
```





# 三、图



## 3.1 图的构造



## 3.2 DFS



## 3.3 BFS



## 3.4 最短路径



## 3.5 最小生成树





# 四、动态规划



# 五、补充

## 5.1 二分



## 5.2 快排



## 5.3 并查集



## 5.4 堆排序



## 5.5 大数和





