# 3. 矩阵基础

矩阵是向量的自然扩展，也是线性代数的核心研究对象。如果说向量是单个数据点，那么矩阵就是数据集或变换规则。本章将系统地介绍矩阵的定义、运算规则及其几何意义——线性变换。

## 3.1 矩阵的定义与表示

### 矩阵的基本概念

**矩阵（Matrix）** 是由数值按行列排列成的矩形阵列。一个 $m \times n$ 的矩阵 $\mathbf{A}$ 包含 $m$ 行 $n$ 列元素：

$$\mathbf{A} = \begin{pmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{pmatrix}$$

矩阵的维度记为 $m \times n$，其中 $m$ 是行数（rows），$n$ 是列数（columns）。例如，一个 $2 \times 3$ 的矩阵有 2 行 3 列。

### 矩阵的元素表示

矩阵 $\mathbf{A}$ 的第 $i$ 行第 $j$ 列元素记为 $a_{ij}$ 或 $(\mathbf{A})_{ij}$。

在 NumPy 中，矩阵可以用二维数组表示：

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

### 矩阵在数据科学中的角色

矩阵在机器学习和数据科学中有多种角色：

**1. 数据集表示**

每行代表一个样本，每列代表一个特征。例如，100 个样本、每个样本 50 个特征的数据集可以表示为 $100 \times 50$ 的矩阵。

```python
# 模拟数据集：100个样本，50个特征
X = np.random.randn(100, 50)
print(f"数据集形状: {X.shape}")  # (100, 50)
```

**2. 线性变换**

矩阵可以表示空间变换。$m \times n$ 的矩阵将 $n$ 维向量映射到 $m$ 维空间。

**3. 权重矩阵**

神经网络中的权重就是矩阵，表示层与层之间的连接强度。

**4. 协方差矩阵**

描述多个随机变量之间的相关性，是对称矩阵。

**5. 图的邻接矩阵**

用矩阵表示图结构，$a_{ij}$ 表示节点 $i$ 和节点 $j$ 之间的连接关系。

## 3.2 矩阵的基本运算

### 矩阵加法

两个维度相同的矩阵可以相加，结果是对应元素相加：

$$(\mathbf{A} + \mathbf{B})_{ij} = a_{ij} + b_{ij}$$

矩阵加法满足：
- 交换律：$\mathbf{A} + \mathbf{B} = \mathbf{B} + \mathbf{A}$
- 结合律：$(\mathbf{A} + \mathbf{B}) + \mathbf{C} = \mathbf{A} + (\mathbf{B} + \mathbf{C})$

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

C = A + B
print("A + B =\n", C)
# [[ 6  8]
#  [10 12]]
```

### 矩阵数乘

标量与矩阵相乘，每个元素都乘以该标量：

$$(c\mathbf{A})_{ij} = c \cdot a_{ij}$$

```python
A = np.array([[1, 2], [3, 4]])
c = 2

result = c * A
print("2 * A =\n", result)
# [[2 4]
#  [6 8]]
```

### 矩阵乘法

**矩阵乘法（Matrix Multiplication）** 是矩阵运算的核心。设 $\mathbf{A}$ 是 $m \times p$ 矩阵，$\mathbf{B}$ 是 $p \times n$ 矩阵，则它们的乘积 $\mathbf{C} = \mathbf{AB}$ 是 $m \times n$ 矩阵：

$$c_{ij} = \sum_{k=1}^{p} a_{ik} b_{kj} = a_{i1}b_{1j} + a_{i2}b_{2j} + \cdots + a_{ip}b_{pj}$$

即 $\mathbf{C}$ 的第 $i$ 行第 $j$ 列元素等于 $\mathbf{A}$ 的第 $i$ 行与 $\mathbf{B}$ 的第 $j$ 列的内积。

```python
A = np.array([[1, 2, 3], [4, 5, 6]])  # 2×3
B = np.array([[7, 8], [9, 10], [11, 12]])  # 3×2

# 方法一：@ 运算符（推荐）
C = A @ B  # 结果是 2×2

# 方法二：np.matmul
C2 = np.matmul(A, B)

# 方法三：np.dot（对于二维数组等同于矩阵乘法）
C3 = np.dot(A, B)

print("A @ B =\n", C)
# [[ 58  64]
#  [139 154]]
```

**重要提醒**：`A * B` 是**逐元素乘法（Hadamard 积）**，不是矩阵乘法！

```python
# Hadamard 积（需要相同维度）
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

hadamard = A * B
print("A * B (Hadamard) =\n", hadamard)
# [[ 5 12]
#  [21 32]]

# 对比矩阵乘法
matrix_mult = A @ B
print("A @ B =\n", matrix_mult)
# [[19 22]
#  [43 50]]
```

### 矩阵乘法的性质

**结合律**：$(\mathbf{AB})\mathbf{C} = \mathbf{A}(\mathbf{BC})$

**分配律**：$\mathbf{A}(\mathbf{B} + \mathbf{C}) = \mathbf{AB} + \mathbf{AC}$

**数乘结合**：$c(\mathbf{AB}) = (c\mathbf{A})\mathbf{B} = \mathbf{A}(c\mathbf{B})$

**转置性质**：$(\mathbf{AB})^T = \mathbf{B}^T \mathbf{A}^T$（注意顺序颠倒）

### 矩阵乘法不满足交换律

一般情况下，$\mathbf{AB} \neq \mathbf{BA}$。这是理解矩阵乘法的关键。

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[0, 1], [1, 0]])

AB = A @ B
BA = B @ A

print("AB =\n", AB)
print("BA =\n", BA)
print(f"AB == BA? {np.array_equal(AB, BA)}")  # False
```

从线性变换的角度，$\mathbf{AB}$ 表示先应用 $\mathbf{B}$ 变换，再应用 $\mathbf{A}$ 变换；而 $\mathbf{BA}$ 表示先应用 $\mathbf{A}$ 变换，再应用 $\mathbf{B}$ 变换。变换顺序不同，结果自然不同。

## 3.3 特殊矩阵

### 单位矩阵（Identity Matrix）

**单位矩阵** $\mathbf{I}$ 是主对角线元素为 1、其余为 0 的方阵：

$$\mathbf{I}_n = \begin{pmatrix}
1 & 0 & \cdots & 0 \\
0 & 1 & \cdots & 0 \\
\vdots & \vdots & \ddots & \vdots \\
0 & 0 & \cdots & 1
\end{pmatrix}$$

单位矩阵是矩阵乘法的"单位元"：$\mathbf{AI} = \mathbf{IA} = \mathbf{A}$。

```python
I = np.eye(3)
print("3×3 单位矩阵:\n", I)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]

A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("A @ I == A:", np.allclose(A @ I, A))  # True
```

### 对角矩阵（Diagonal Matrix）

**对角矩阵** 除主对角线外，其他元素都为 0：

$$\mathbf{D} = \begin{pmatrix}
d_1 & 0 & 0 \\
0 & d_2 & 0 \\
0 & 0 & d_3
\end{pmatrix}$$

对角矩阵的运算非常高效：

```python
# 从对角元素创建对角矩阵
d = np.array([1, 2, 3])
D = np.diag(d)
print("对角矩阵:\n", D)
# [[1 0 0]
#  [0 2 0]
#  [0 0 3]]

# 对角矩阵乘法等同于缩放
v = np.array([4, 5, 6])
result = D @ v
print("D @ v =", result)  # [4, 10, 18] = [1*4, 2*5, 3*6]
```

对角矩阵左乘向量，相当于对向量的每个分量进行独立缩放。

### 对称矩阵（Symmetric Matrix）

**对称矩阵** 满足 $\mathbf{A} = \mathbf{A}^T$，即 $a_{ij} = a_{ji}$。

对称矩阵的重要性质：
- 特征值都是实数
- 特征向量可以构成正交基
- 协方差矩阵、邻接矩阵、Hessian 矩阵都是对称矩阵

```python
# 创建对称矩阵
A = np.array([[1, 2, 3], [2, 4, 5], [3, 5, 6]])
print("对称矩阵:\n", A)
print("A == A.T:", np.allclose(A, A.T))  # True
```

### 正交矩阵（Orthogonal Matrix）

**正交矩阵** 满足 $\mathbf{Q}^T \mathbf{Q} = \mathbf{I}$，即其转置等于其逆：

$$\mathbf{Q}^{-1} = \mathbf{Q}^T$$

正交矩阵的几何意义：它保持向量的长度和角度不变，只进行旋转或反射。

```python
# 旋转矩阵是正交矩阵
theta = np.pi / 4  # 45度
Q = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta), np.cos(theta)]
])

print("Q^T @ Q =\n", Q.T @ Q)  # 接近单位矩阵
print("是正交矩阵:", np.allclose(Q.T @ Q, np.eye(2)))  # True
```

### 三角矩阵

**上三角矩阵**：主对角线以下的元素全为 0。

**下三角矩阵**：主对角线以上的元素全为 0。

三角矩阵在求解线性方程组（如高斯消元法）中非常重要。

```python
A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

upper = np.triu(A)  # 上三角
lower = np.tril(A)  # 下三角

print("上三角矩阵:\n", upper)
print("下三角矩阵:\n", lower)
```

## 3.4 矩阵的转置

### 转置的定义

**转置（Transpose）** 是将矩阵的行列互换的操作。设 $\mathbf{A}$ 是 $m \times n$ 矩阵，其转置 $\mathbf{A}^T$ 是 $n \times m$ 矩阵：

$$(\mathbf{A}^T)_{ij} = a_{ji}$$

```python
A = np.array([[1, 2, 3], [4, 5, 6]])  # 2×3
A_T = A.T  # 3×2

print("原矩阵 (2×3):\n", A)
print("转置后 (3×2):\n", A_T)
# [[1 4]
#  [2 5]
#  [3 6]]
```

### 转置的性质

1. $(\mathbf{A}^T)^T = \mathbf{A}$（转置的转置等于自身）
2. $(\mathbf{A} + \mathbf{B})^T = \mathbf{A}^T + \mathbf{B}^T$
3. $(c\mathbf{A})^T = c\mathbf{A}^T$
4. $(\mathbf{AB})^T = \mathbf{B}^T \mathbf{A}^T$（乘积的转置等于转置的反向乘积）

性质 4 特别重要，它在反向传播算法中经常出现。

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 验证 (AB)^T = B^T A^T
left = (A @ B).T
right = B.T @ A.T

print("(AB)^T == B^T A^T:", np.allclose(left, right))  # True
```

### 对称矩阵与转置

对称矩阵 $\mathbf{A}$ 满足 $\mathbf{A} = \mathbf{A}^T$。任何矩阵 $\mathbf{B}$ 都可以通过 $\mathbf{B} + \mathbf{B}^T$ 或 $\mathbf{B}\mathbf{B}^T$ 构造对称矩阵：

```python
B = np.array([[1, 2], [3, 4]])

# 方法一：B + B^T
sym1 = B + B.T
print("B + B^T:\n", sym1)

# 方法二：B @ B^T（结果是对称正定矩阵）
sym2 = B @ B.T
print("B @ B^T:\n", sym2)
```

## 3.5 矩阵的逆

### 可逆矩阵的定义

对于方阵 $\mathbf{A}$，如果存在矩阵 $\mathbf{B}$ 使得：

$$\mathbf{AB} = \mathbf{BA} = \mathbf{I}$$

则称 $\mathbf{A}$ **可逆（Invertible）**，$\mathbf{B}$ 称为 $\mathbf{A}$ 的**逆矩阵**，记为 $\mathbf{A}^{-1}$。

并非所有方阵都可逆。矩阵可逆的条件：
- 行列式不为零：$\det(\mathbf{A}) \neq 0$
- 满秩：$\text{rank}(\mathbf{A}) = n$（对于 $n \times n$ 矩阵）
- 所有特征值都不为零

```python
A = np.array([[1, 2], [3, 4]])

# 计算逆矩阵
A_inv = np.linalg.inv(A)

print("逆矩阵:\n", A_inv)
print("验证 A @ A_inv:\n", A @ A_inv)  # 接近单位矩阵
print("验证 A_inv @ A:\n", A_inv @ A)  # 接近单位矩阵
```

### 逆矩阵的性质

1. $(\mathbf{A}^{-1})^{-1} = \mathbf{A}$
2. $(\mathbf{AB})^{-1} = \mathbf{B}^{-1} \mathbf{A}^{-1}$（注意顺序颠倒）
3. $(\mathbf{A}^T)^{-1} = (\mathbf{A}^{-1})^T$
4. $(c\mathbf{A})^{-1} = \frac{1}{c}\mathbf{A}^{-1}$（当 $c \neq 0$）

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 验证 (AB)^-1 = B^-1 A^-1
left = np.linalg.inv(A @ B)
right = np.linalg.inv(B) @ np.linalg.inv(A)

print("(AB)^-1 == B^-1 A^-1:", np.allclose(left, right))  # True
```

### 伪逆（Moore-Penrose 伪逆）

当矩阵不可逆或不是方阵时，可以使用**伪逆（Pseudoinverse）** $\mathbf{A}^+$：

$$\mathbf{A}^+ = (\mathbf{A}^T \mathbf{A})^{-1} \mathbf{A}^T$$（当 $\mathbf{A}^T \mathbf{A}$ 可逆时）

伪逆满足：
- $\mathbf{A}\mathbf{A}^+\mathbf{A} = \mathbf{A}$
- $\mathbf{A}^+\mathbf{A}\mathbf{A}^+ = \mathbf{A}^+$
- $(\mathbf{A}\mathbf{A}^+)^T = \mathbf{A}\mathbf{A}^+$
- $(\mathbf{A}^+\mathbf{A})^T = \mathbf{A}^+\mathbf{A}$

伪逆在最小二乘法中有重要应用。

```python
# 非方阵的伪逆
A = np.array([[1, 2], [3, 4], [5, 6]])  # 3×2 矩阵

A_pinv = np.linalg.pinv(A)
print("伪逆形状:", A_pinv.shape)  # (2, 3)

# 验证伪逆性质
print("A @ A+ @ A ≈ A:", np.allclose(A @ A_pinv @ A, A))
print("A+ @ A @ A+ ≈ A+:", np.allclose(A_pinv @ A @ A_pinv, A_pinv))
```

## 3.6 线性变换的几何意义

矩阵乘法的几何意义是**线性变换（Linear Transformation）**。当一个矩阵左乘一个向量时，它对该向量进行了变换。

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