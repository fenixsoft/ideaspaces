# 矩阵基础

矩阵是向量的自然扩展，也是线性代数的核心研究对象。如果说向量是单个数据点，那么矩阵就是数据集或变换规则。本章将系统地介绍矩阵的定义、运算规则及其几何意义 —— 线性变换。

## 矩阵的概念与应用

**矩阵（Matrix）** 是由标量按行列排列成的矩形阵列，如向量将标量从零阶扩展到一阶，矩阵则把向量从一阶扩展到了二阶。习惯上，人们常用粗体、大写字母来表示矩阵。一个 $m \times n$ 的矩阵 $\mathbf{A}$ 包含 $m$ 行 $n$ 列元素。矩阵的维度记为 $m \times n$，其中 $m$ 是行数（rows），$n$ 是列数（columns）。矩阵具有相同数量的行和列时被成为**方阵（Square Matrix）**，其形状为正方形。

$$ \mathbf{A} = \begin{pmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{pmatrix} $$

矩阵 $\mathbf{A}$ 的第 $i$ 行第 $j$ 列元素记为 $a_{ij}$ 或 $(\mathbf{A})_{ij}$。在 NumPy 中，矩阵可以用二维数组表示，譬如，一个 $2 \times 3$ 的矩阵有 2 行 3 列：

```python
import numpy as np

# 创建 2×3 矩阵
A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

print(f"矩阵形状: {A.shape}")     # (2, 3)
print(f"行数: {A.shape[0]}")      # 2
print(f"列数: {A.shape[1]}")      # 3
print(f"元素 a[0,1]: {A[0, 1]}")  # 2（第0行第1列，0-indexed）
```
矩阵在机器学习和数据科学中有广泛应用。可以把矩阵想象成 Excel 的数据表，通过行、列参数就能定为到数据，但它能做的远不止存储数据。列举一些例子：

 - **数据集表示**：矩阵是机器学习的"原材料"，把矩阵想象成一张数据表格：每行是一个样本（比如一位用户、一张图片），每列是一个特征（比如年龄、价格、像素值）。这种结构让计算机能高效处理成千上万的数据点。

 - **线性变换**：矩阵是数据的"转换器"，矩阵就像一台变形机器，能把数据从一种形态转换成另一种。比如把二维平面上的点旋转45度，或者把三维物体投影到二维屏幕——这些操作都可以用矩阵乘法表示。$m \times n$ 的矩阵可以将 $n$ 维的数据"压缩"或"扩展"成 $m$ 维。这在降维（如PCA）中特别有用：把高维复杂数据变成低维简洁表示。

 - **权重矩阵**：矩阵是神经网络的"记忆"，神经网络的核心就是权重矩阵。想象大脑神经元之间的连接：有的连接强，有的弱。权重矩阵记录了这些连接强度——矩阵的每个元素 $w_{ij}$ 表示"第 $i$ 个神经元对第 $j$ 个神经元的影响有多大"。神经网络学习的过程，本质上就是在调整这些权重矩阵中的数值。

 - **协方差矩阵**：矩阵是变量间的"默契度"，协方差矩阵回答一个问题：这些变量是怎么一起变动的？

    - 正数表示正相关，"同进退"（气温和冰淇淋销量）
    - 负数表示负相关，"唱反调"（海拔和气温）
    - 接近零表示不相关，"各玩各的"（智商和鞋码）

    显然，协方差矩阵肯定是对称的 —— 因为变量 A 和 B 的关系，与 B 和 A 的关系说的其实就是同一件事情。

 - **邻接矩阵**：矩阵是关系的"地图"，社交网络、交通路线、网页链接——都可以用邻接矩阵表示。矩阵中 $a_{ij}$ 表示"从节点 $i$ 到节点 $j$ 是否有连接"。这种表示让图算法（如PageRank、推荐系统）能够高效计算。


## 矩阵的运算

跟向量一样，矩阵同样支持加法、数乘、乘法运算，但是有一些前提约束：两个矩阵必须具有相同的维度（相同的行数和列数）才能够进行加法运算，两个矩阵必须满足第一个矩阵的列数必须等于第二个矩阵的行数（内维匹配）才能进行乘法运算。

- **矩阵加法**：矩阵相加的结果是对应元素相加：$(\mathbf{A} + \mathbf{B})_{ij} = a_{ij} + b_{ij}$，矩阵加法满足：
    - 交换律：$\mathbf{A} + \mathbf{B} = \mathbf{B} + \mathbf{A}$
    - 结合律：$(\mathbf{A} + \mathbf{B}) + \mathbf{C} = \mathbf{A} + (\mathbf{B} + \mathbf{C})$

- **矩阵数乘**：标量与矩阵相乘，每个元素都乘以该标量：$(c\mathbf{A})_{ij} = c \cdot a_{ij}$

- **矩阵乘法**：矩阵乘法（Matrix Multiplication）是矩阵运算的核心。设 $\mathbf{A}$ 是 $m \times p$ 矩阵，$\mathbf{B}$ 是 $p \times n$ 矩阵，则它们的乘积 $\mathbf{C} = \mathbf{AB}$ 是 $m \times n$ 矩阵：$c_{ij} = \sum_{k=1}^{p} a_{ik} b_{kj} = a_{i1}b_{1j} + a_{i2}b_{2j} + \cdots + a_{ip}b_{pj}$。即 $\mathbf{C}$ 的第 $i$ 行第 $j$ 列元素等于 $\mathbf{A}$ 的第 $i$ 行与 $\mathbf{B}$ 的第 $j$ 列的内积。矩阵乘法满足：

    - 结合律：$(\mathbf{AB})\mathbf{C} = \mathbf{A}(\mathbf{BC})$
    - 数乘结合律：$c(\mathbf{AB}) = (c\mathbf{A})\mathbf{B} = \mathbf{A}(c\mathbf{B})$
    - 分配律：$\mathbf{A}(\mathbf{B} + \mathbf{C}) = \mathbf{AB} + \mathbf{AC}$

    但是注意，矩阵乘法不满足交换律，一般情况下，$\mathbf{AB} \neq \mathbf{BA}$。甚至于 $\mathbf{BA}$ 都未必是一个合法的结果，它不一定能满足内维匹配要求。

从代数角度看，矩阵乘法运算十分繁琐，但是它的几何意义却十分简洁（见本章的线性变换一节），这人类理解矩阵乘法的捷径，代数公式那是留给计算机去用的。

另外，特别提醒一下，矩阵乘法的写法就是“$\mathbf{AB}$”，并不是像初等代数乘法那样，中间省略了乘号。如果在文献中看到 $\mathbf{A} * \mathbf{B}$ 或者 $\mathbf{A} \circ \mathbf{B}$，所指的其实是矩阵的 Hadamard 积（逐元素乘积），而非矩阵乘法，它是指两个维度完全一样的矩阵，对应位置的元素组个相乘，形成另一个维度一样的矩阵： $(\mathbf{A} \odot \mathbf{B}){ij} = a{ij} \cdot b_{ij} \quad (1 \leq i \leq m,\ 1 \leq j \leq n)$

## 矩阵的转置和逆

除加法、数乘、乘法外，矩阵还有“转置”和“逆”两种常用种的一元运算：

- **矩阵的转置（Transpose）** 是一种将矩阵的行列互换的操作。设 $\mathbf{A}$ 是 $m \times n$ 矩阵，其转置 $\mathbf{A}^T$ 是 $n \times m$ 矩阵：$(\mathbf{A}^T)_{ij} = a_{ji}$。转置具备如下性质：

    - $(\mathbf{A}^T)^T = \mathbf{A}$（转置的转置等于自身）
    - $(\mathbf{A} + \mathbf{B})^T = \mathbf{A}^T + \mathbf{B}^T$
    - $(c\mathbf{A})^T = c\mathbf{A}^T$
    - $(\mathbf{AB})^T = \mathbf{B}^T \mathbf{A}^T$（乘积的转置等于转置的反向乘积）

    后续学习误差方向传播算法时会反复用到第 4 条性质，$(\mathbf{AB})^T = \mathbf{B}^T\mathbf{A}^T$ 确保了反向传播时梯度能够正确地"逆流"回每一层，保持维度匹配，这是自动微分和深度学习框架（PyTorch、TensorFlow）能够高效计算梯度的数学基础。

- **矩阵的逆（Inverse）** 是一种"撤销"原矩阵的线性变换，回到原始状态的操作。对于方阵 $\mathbf{A}$，如果存在矩阵 $\mathbf{B}$ 使得：$\mathbf{AB} = \mathbf{BA} = \mathbf{I}$，则称 $\mathbf{A}$ 可逆（Invertible），$\mathbf{B}$ 称为 $\mathbf{A}$ 的逆矩阵，记为 $\mathbf{A}^{-1}$。逆矩阵具备如下性质：

    - $(\mathbf{A}^{-1})^{-1} = \mathbf{A}$（撤销的撤销 = 原样。就像"取消撤销"就是回到最初的样子）
    - $(\mathbf{AB})^{-1} = \mathbf{B}^{-1} \mathbf{A}^{-1}$（先穿袜子再穿鞋，脱的时候要倒过来：先脱鞋再脱袜子）
    - $(\mathbf{A}^T)^{-1} = (\mathbf{A}^{-1})^T$（转置和求逆可以交换顺序）
    - $(c\mathbf{A})^{-1} = \frac{1}{c}\mathbf{A}^{-1}, c \neq 0$（放大 $c$ 倍的变换，其逆就是缩小 $\frac{1}{c}$）

    并非所有方阵都可逆。矩阵可逆的条件，需要同时满足行列式不为零（$\det(\mathbf{A}) \neq 0$）、满秩（$\text{rank}(\mathbf{A}) = n$，对于 $n \times n$ 矩阵）和所有特征值都不为零这三个条件的方阵才可逆。当矩阵不可逆或不是方阵时，可以使用 **伪逆（Pseudoinverse）** 获得一个最接近的近似解。伪逆记为 $\mathbf{A}^+$，含义为：$\mathbf{A}^+ = (\mathbf{A}^T \mathbf{A})^{-1} \mathbf{A}^T$（当 $\mathbf{A}^T \mathbf{A}$ 可逆时）。伪逆具备如下性质：

    - $\mathbf{A}\mathbf{A}^+\mathbf{A} = \mathbf{A}$
    - $\mathbf{A}^+\mathbf{A}\mathbf{A}^+ = \mathbf{A}^+$
    - $(\mathbf{A}\mathbf{A}^+)^T = \mathbf{A}\mathbf{A}^+$
    - $(\mathbf{A}^+\mathbf{A})^T = \mathbf{A}^+\mathbf{A}$

    不要靠记忆代数公式来理解矩阵的逆，先从逆矩阵的意图上去理解它（笔者在公式后面的文字注释）。将矩阵理解为对数据进行某些变换，不妨更具体一些，将这些变换想象成你对图片的 PS 的操作，你想图片完全恢复原状这就是求逆矩阵 $\mathbf{A}^{-1}$。图片能够完美恢复的前提是变换不会产生有效信息丢失：行列式为零就代表把一个维度完全压扁了，有效信息丢了；不满秩就表示部分信息是冗余的，有效信息丢了；特征值为零代表某个方向上信息完全"塌陷"掉，有效信息丢了，只要丢失了有效信息，就不再可能完美复原数据。


## 特殊矩阵

在矩阵运算中，有一类矩阵因其简洁的结构而具有特殊的代数性质。它们就像是数字世界中的"基石"——虽然形式简单，却能简化复杂的运算、揭示问题的本质，并在求解线性方程组、坐标变换等场景中扮演关键角色。下面介绍几种最重要的特殊矩阵：

- **单位矩阵（Identity Matrix）**：$\mathbf{I}$ 是主对角线元素为 1、其余为 0 的方阵，单位矩阵是矩阵乘法的"单位元"，满足： $\mathbf{AI} = \mathbf{IA} = \mathbf{A}$。

    $$\mathbf{I}_n = \begin{pmatrix}
    1 & 0 & \cdots & 0 \\
    0 & 1 & \cdots & 0 \\
    \vdots & \vdots & \ddots & \vdots \\
    0 & 0 & \cdots & 1
    \end{pmatrix}$$

- **对角矩阵（Diagonal Matrix）**：对角矩阵除主对角线外，其他元素都为 0 的方阵，对角矩阵左乘向量，相当于对向量的每个分量进行独立缩放。

    $$\mathbf{D} = \begin{pmatrix}
    d_1 & 0 & 0 \\
    0 & d_2 & 0 \\
    0 & 0 & d_3
    \end{pmatrix}$$

- **对称矩阵（Symmetric Matrix）**：对称矩阵满足 $\mathbf{A} = \mathbf{A}^T$，即 $a_{ij} = a_{ji}$。对称矩阵包含的特征向量可以构成正交基，许多有用的矩阵如协方差矩阵、邻接矩阵、Hessian 矩阵都是对称矩阵

- **正交矩阵（Orthogonal Matrix）**：正交矩阵满足 $\mathbf{Q}^T \mathbf{Q} = \mathbf{I}$，即其转置等于其逆：$\mathbf{Q}^{-1} = \mathbf{Q}^T$。正交矩阵的作用在于它保持向量的长度和角度不变，只进行旋转或反射。

## 线性变换

### 矩阵-向量积

**数学定义**：给定矩阵 $\mathbf{A}$（假设为 2×2）和向量 $\vec{v} = \begin{pmatrix} v_1 \\ v_2 \end{pmatrix}$，矩阵与向量的乘法定义为：

$$\mathbf{A}\vec{v} = v_1 \cdot \vec{a_1} + v_2 \cdot \vec{a_2}$$

其中 $\vec{a_1}$ 和 $\vec{a_2}$ 分别是矩阵 $\mathbf{A}$ 的第一列和第二列。这意味着：**把矩阵的每一列看作一个"基向量"，把向量 $\vec{v}$ 的分量看作在这些方向上的"步数"**。

---

**通俗理解**：想象你在一张地图上，矩阵 $\mathbf{A}$ 的两列就像是两张"传送门卡片"——第一张卡片（第一列）把你送到某个位置，第二张卡片（第二列）把你送到另一个位置。向量 $\vec{v}$ 的分量 $v_1$ 和 $v_2$ 告诉你：先沿着第一张卡片的方向走 $v_1$ 步，再沿着第二张卡片的方向走 $v_2$ 步，最后到达的地方就是你的目的地。

比如 $v_1=2, v_2=3$ 意味着：走 2 次第一列的方向，再走 3 次第二列的方向，加起来就是你最终的位置。这就是矩阵如何把"旧坐标"变成"新坐标"的。





矩阵乘法的几何意义是**对空间进行变形（线性变换）**。你可以把矩阵看作一个"变形规则"，当矩阵左乘一个向量时，它按照这个规则把原向量"搬"到一个新的位置。

具体来说，矩阵的每一列代表一个基向量变换后的新位置。例如，2×2 矩阵的第一列是原来 x 轴方向的单位向量 $(1,0)$ 变换后的落脚点，第二列是原来 y 轴方向的单位向量 $(0,1)$ 变换后的落脚点。整个空间就像一张被拉伸、旋转或剪切的橡皮布，而矩阵记录了每个坐标轴"搬到哪里去了"。



### 线性变换的定义

**线性变换** $T$ 满足两条性质：
1. 可加性：$T(\mathbf{u} + \mathbf{v}) = T(\mathbf{u}) + T(\mathbf{v})$
2. 齐次性：$T(c\mathbf{v}) = cT(\mathbf{v})$

线性变换保持直线和平行线——这是理解神经网络的关键：每一层都是一个线性变换（后接非线性激活函数）。

### 缩放变换

**缩放矩阵** 沿坐标轴方向拉伸或压缩：

$$\mathbf{S} = \begin{pmatrix} s_x & 0 \\ 0 & s_y \end{pmatrix}$$

当 $s_x = s_y$ 时为均匀缩放；否则为非均匀缩放。

```python
import numpy as np
import matplotlib.pyplot as plt

# 定义原始单位正方形
square = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]).T

# 缩放矩阵：x 放大 2 倍，y 放大 1.5 倍
S = np.array([[2, 0], [0, 1.5]])

# 应用变换
transformed = S @ square

# 可视化
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(square[0], square[1], 'b-', linewidth=2, label='原始')
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.title('原始正方形')

plt.subplot(1, 2, 2)
plt.plot(transformed[0], transformed[1], 'r-', linewidth=2, label='缩放后')
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.title('缩放变换 (Sx=2, Sy=1.5)')

plt.tight_layout()
plt.savefig('scaling_transform.png', dpi=150)
plt.close()
print("缩放变换图示已保存")
```

### 旋转变换

**旋转矩阵** 将向量绕原点旋转角度 $\theta$（逆时针为正）：

$$\mathbf{R} = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$$

旋转矩阵是正交矩阵，保持向量长度不变。

```python
# 旋转矩阵：逆时针旋转 45 度
theta = np.pi / 4
R = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta), np.cos(theta)]
])

# 验证正交性
print("R^T @ R =\n", R.T @ R)
print("是正交矩阵:", np.allclose(R.T @ R, np.eye(2)))

# 应用旋转
v = np.array([1, 0])
rotated_v = R @ v
print(f"向量 {v} 旋转 45° 后: {rotated_v.round(3)}")
```

### 剪切变换

**剪切矩阵** 使形状"倾斜"：

$$\mathbf{H}_x = \begin{pmatrix} 1 & k \\ 0 & 1 \end{pmatrix}$$

这是沿 x 方向的剪切，参数 $k$ 控制剪切程度。

```python
# 沿 x 方向剪切
k = 0.5
H = np.array([[1, k], [0, 1]])

# 应用剪切
v = np.array([0, 1])
sheared_v = H @ v
print(f"向量 {v} 剪切后: {sheared_v}")  # [0.5, 1]
```

### 组合变换

多个变换可以通过矩阵乘法组合：

$$\mathbf{M} = \mathbf{R}_2 \cdot \mathbf{S} \cdot \mathbf{R}_1$$

表示先旋转 $\mathbf{R}_1$，再缩放 $\mathbf{S}$，最后旋转 $\mathbf{R}_2$。

**注意**：矩阵乘法从右向左应用，所以顺序很重要。

```python
# 组合变换：先旋转 30°，再缩放
theta = np.pi / 6  # 30度
R = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta), np.cos(theta)]
])
S = np.array([[2, 0], [0, 0.5]])

# 组合：先 R 后 S
M = S @ R

# 应用到向量
v = np.array([1, 0])
transformed = M @ v
print(f"变换后: {transformed.round(3)}")
```

### 神经网络层与线性变换

神经网络的全连接层本质上就是线性变换：

$$\mathbf{y} = \mathbf{W}\mathbf{x} + \mathbf{b}$$

其中 $\mathbf{W}$ 是权重矩阵，$\mathbf{x}$ 是输入向量，$\mathbf{b}$ 是偏置向量，$\mathbf{y}$ 是输出向量。

```python
import torch
import torch.nn as nn

# 定义一个全连接层
layer = nn.Linear(784, 128)

# 前向传播
x = torch.randn(32, 784)  # 批量大小 32
y = layer(x)

print(f"输入形状: {x.shape}")       # (32, 784)
print(f"输出形状: {y.shape}")       # (32, 128)
print(f"权重形状: {layer.weight.shape}")  # (128, 784)
print(f"偏置形状: {layer.bias.shape}")    # (128,)

# 数学等价于：y = x @ W.T + b
```

多层神经网络就是多个线性变换的复合（中间有非线性激活函数）。理解矩阵乘法的几何意义，有助于直观理解神经网络如何变换数据。

---

## 本章小结

本章介绍了矩阵的核心概念：

1. **矩阵定义**：数值的矩形阵列，可表示数据集或线性变换
2. **矩阵运算**：加法、数乘、乘法，乘法是核心但不可交换
3. **特殊矩阵**：单位矩阵、对角矩阵、对称矩阵、正交矩阵、三角矩阵
4. **转置与逆**：重要的矩阵操作，伪逆处理不可逆情况
5. **线性变换**：矩阵乘法的几何意义，神经网络的基础

下一章将介绍如何使用 Python 和 NumPy 进行实际的矩阵操作。