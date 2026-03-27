# 2. 向量基础

向量是线性代数最基本的研究对象，也是理解机器学习算法的关键。本章将系统地介绍向量的定义、运算规则及其几何意义，为后续章节奠定坚实基础。

## 2.1 向量的定义与表示

### 数学定义：有序数值序列

**向量（Vector）** 是由一组有序数值组成的序列。在数学上，$n$ 维向量 $\mathbf{v}$ 定义为：

$$\mathbf{v} = (v_1, v_2, \ldots, v_n)$$

其中 $v_i$ 称为向量的第 $i$ 个**分量（Component）**，$n$ 称为向量的**维度（Dimension）**。譬如，$\mathbf{v} = (3, -1, 2)$ 是一个三维向量，其三个分量分别为 $v_1 = 3$，$v_2 = -1$，$v_3 = 2$。

向量有列向量与行向量两种常见的表示形式：

- **行向量**：分量水平排列
$$\mathbf{v} = \begin{bmatrix} v_1 & v_2 & \cdots & v_n \end{bmatrix}$$

- **列向量**：分量垂直排列
$$\mathbf{v} = \begin{pmatrix} v_1 \\ v_2 \\ \vdots \\ v_n \end{pmatrix}$$

在大多数线性代数文献和机器学习框架中，默认使用**列向量**。在 Python/NumPy 中，一维数组既可以表示行向量也可以表示列向量：

```python
import numpy as np

# 一维数组（默认表示向量）
v = np.array([3, -1, 2])
print(f"形状: {v.shape}")  # (3,) - 一维数组

# 明确的行向量（二维数组）
row_vector = v.reshape(1, -1)
print(f"行向量形状: {row_vector.shape}")  # (1, 3)

# 明确的列向量（二维数组）
col_vector = v.reshape(-1, 1)
print(f"列向量形状: {col_vector.shape}")  # (3, 1)
```

### 向量空间（Vector Space）的公理化定义

**向量空间** 是一个更抽象的数学概念。设 $V$ 是一个非空集合，$\mathbb{F}$ 是一个数域（通常是实数域 $\mathbb{R}$），如果 $V$ 中定义了加法和数乘两种运算，且满足以下八条公理，则称 $V$ 是 $\mathbb{F}$ 上的向量空间：

**加法公理（4条）**：
1. 交换律：$\mathbf{u} + \mathbf{v} = \mathbf{v} + \mathbf{u}$
2. 结合律：$(\mathbf{u} + \mathbf{v}) + \mathbf{w} = \mathbf{u} + (\mathbf{v} + \mathbf{w})$
3. 零向量存在：存在 $\mathbf{0}$ 使得 $\mathbf{v} + \mathbf{0} = \mathbf{v}$
4. 逆元存在：对任意 $\mathbf{v}$，存在 $-\mathbf{v}$ 使得 $\mathbf{v} + (-\mathbf{v}) = \mathbf{0}$

**数乘公理（4条）**：

5. 数乘与向量加法分配：$c(\mathbf{u} + \mathbf{v}) = c\mathbf{u} + c\mathbf{v}$
6. 数乘与标量加法分配：$(c + d)\mathbf{v} = c\mathbf{v} + d\mathbf{v}$
7. 数乘结合律：$c(d\mathbf{v}) = (cd)\mathbf{v}$
8. 单位元：$1 \cdot \mathbf{v} = \mathbf{v}$

这些公理严格保证了向量运算的基本性质，但是对于非数学专业的读者，它们确实拗口。笔者建议不妨将向量空间想想成一张无限大的白纸，只要一个集合里的元素能进行以下“加法”和“乘法”两种运算：

1. 加法：从原点出发，先走向量 a 再走向量 b，等价于直接走 a + b
2. 数乘：能把向量 a 拉长2倍变成 2a，或反向翻转变成 -a

显然，无论“加法”还是“乘法”如何折腾，得到结果还在这个张无限大的白纸里面（封闭性），并且这些操作都满足结合律、分配律等"自然"的算术规则，那这张白纸就是一个向量空间。无论是严格的八条公理，还是白纸上做加法乘法的通俗理解，其实都在说一件事儿：向量空间里面的东西能互相"加减"和"缩放"，且怎么折腾都不会跑出这个集合。在机器学习中，我们主要关注**欧几里得空间** $\mathbb{R}^n$，即所有 $n$ 维实数向量的集合。

### 线性相关与线性无关

如果给定一组向量 $\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_k$，如果存在不全为零的标量 $c_1, c_2, \ldots, c_k$，使得：

$$c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + \cdots + c_k\mathbf{v}_k = \mathbf{0}$$

则称这组向量**线性相关（Linearly Dependent）**。否则，如果只有 $c_1 = c_2 = \cdots = c_k = 0$ 才能使上式成立，则称这组向量**线性无关（Linearly Independent）**。

这两个定义的直观解释是：线性无关意味着没有任何一个向量可以被其他向量表示，好比一个由程序员、设计师、产品经理组成的团队，每个成员都有独特的技能，没有人能替代其他人；线性相关意味着至少有一个向量可以由其他向量的线性组合表示，相当于团队中有人是"多余的"，他能做的工作别人也能做。

在机器学习和模型训练中要经常使用 **秩（Rank）** 这个概念，它就直接来源于线性相关与线性无关。

- **特征选择**：如果特征矩阵的秩小于特征数，说明存在冗余特征
- **数据压缩**：秩分解可以实现低秩近似，用更少参数近似原矩阵，降低维度减少存储
- **奇异值分解**：秩等同于非零奇异值个数，决定了"有多少东西值得保留"

秩就是指向量组中线性无关向量的最大个数。对于一个矩阵，其秩等于其行向量组的秩，也等于其列向量组的秩。因此我们可以通过如下代码，判断向量是否线性相关。

```python
import numpy as np
from numpy.linalg import matrix_rank

# 判断向量组是否线性相关
def is_linearly_independent(vectors):
    """
    通过矩阵秩判断向量组是否线性无关
    如果秩等于向量个数，则线性无关
    """
    A = np.column_stack(vectors)  # 将向量组成矩阵
    rank = matrix_rank(A)
    return rank == len(vectors)

# 示例：三维空间中的三个向量
v1 = np.array([1, 0, 0])
v2 = np.array([0, 1, 0])
v3 = np.array([0, 0, 1])  # 与 v1, v2 线性无关

v4 = np.array([1, 1, 0])  # v4 = v1 + v2，与 v1, v2 线性相关

print(f"v1, v2, v3 线性无关: {is_linearly_independent([v1, v2, v3])}")  # True
print(f"v1, v2, v4 线性无关: {is_linearly_independent([v1, v2, v4])}")  # False
```


## 2.2 向量加法与数乘

向量加法和数乘是向量空间最基本的两种运算，它们构成了线性代数的基础。

### 向量加法：平行四边形法则与三角形法则

**向量加法**定义如下：对于两个同维向量 $\mathbf{u} = (u_1, \ldots, u_n)$ 和 $\mathbf{v} = (v_1, \ldots, v_n)$：

$$\mathbf{u} + \mathbf{v} = (u_1 + v_1, u_2 + v_2, \ldots, u_n + v_n)$$

在几何上，向量加法有两种等价的图解方法：

**平行四边形法则**：将两个向量 $\mathbf{u}$ 和 $\mathbf{v}$ 的起点放在同一点，以它们为邻边作平行四边形，从公共起点出发的对角线就是 $\mathbf{u} + \mathbf{v}$。

**三角形法则**：将 $\mathbf{v}$ 的起点放在 $\mathbf{u}$ 的终点，从 $\mathbf{u}$ 的起点到 $\mathbf{v}$ 的终点的向量就是 $\mathbf{u} + \mathbf{v}$。

```
平行四边形法则:                三角形法则:

    v ────→ ●                   u ────→ ●
    │      /                            /
    │    /   u+v                        / v
    │  /                              /
    ● ←──── u                       ●
```

```python
import numpy as np
import matplotlib.pyplot as plt

# 向量加法可视化
def plot_vector_addition():
    u = np.array([2, 1])
    v = np.array([1, 2])
    w = u + v

    plt.figure(figsize=(10, 5))

    # 左图：平行四边形法则
    plt.subplot(1, 2, 1)
    plt.quiver(0, 0, u[0], u[1], angles='xy', scale_units='xy', scale=1, color='r', label='u')
    plt.quiver(0, 0, v[0], v[1], angles='xy', scale_units='xy', scale=1, color='b', label='v')
    plt.quiver(0, 0, w[0], w[1], angles='xy', scale_units='xy', scale=1, color='g', label='u+v')
    plt.quiver(u[0], u[1], v[0], v[1], angles='xy', scale_units='xy', scale=1, color='b', alpha=0.3)
    plt.quiver(v[0], v[1], u[0], u[1], angles='xy', scale_units='xy', scale=1, color='r', alpha=0.3)
    plt.xlim(-0.5, 4)
    plt.ylim(-0.5, 4)
    plt.grid(True)
    plt.legend()
    plt.title('平行四边形法则')

    # 右图：三角形法则
    plt.subplot(1, 2, 2)
    plt.quiver(0, 0, u[0], u[1], angles='xy', scale_units='xy', scale=1, color='r', label='u')
    plt.quiver(u[0], u[1], v[0], v[1], angles='xy', scale_units='xy', scale=1, color='b', label='v')
    plt.quiver(0, 0, w[0], w[1], angles='xy', scale_units='xy', scale=1, color='g', label='u+v')
    plt.xlim(-0.5, 4)
    plt.ylim(-0.5, 4)
    plt.grid(True)
    plt.legend()
    plt.title('三角形法则')

    plt.tight_layout()
    plt.savefig('vector_addition.png', dpi=150)
    plt.close()

# 执行可视化
plot_vector_addition()
print("向量加法图示已保存")
```

### 数乘：伸缩效果

**数乘（Scalar Multiplication）** 定义为标量与向量的乘积：

$$c\mathbf{v} = (cv_1, cv_2, \ldots, cv_n)$$

几何意义：
- 当 $c > 0$：向量的长度变为原来的 $|c|$ 倍，方向不变
- 当 $c < 0$：向量的长度变为原来的 $|c|$ 倍，方向反向
- 当 $c = 0$：结果为零向量 $\mathbf{0}$

```python
v = np.array([1, 2])

# 不同标量的数乘效果
scalars = [0.5, 1, 2, -1, -2]
for c in scalars:
    result = c * v
    print(f"{c} × {v} = {result}")
```

### 线性组合与线性生成

**线性组合（Linear Combination）** 是向量加法和数乘的复合运算。给定向量 $\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_k$ 和标量 $c_1, c_2, \ldots, c_k$，表达式：

$$c_1\mathbf{v}_1 + c_2\mathbf{v}_2 + \cdots + c_k\mathbf{v}_k$$

称为这些向量的线性组合。

**线性生成（Span）**：向量组 $\mathbf{v}_1, \ldots, \mathbf{v}_k$ 的所有线性组合构成的集合，记为 $\text{span}(\mathbf{v}_1, \ldots, \mathbf{v}_k)$。

在机器学习中，线性组合是神经网络的基础：每一层的输出就是前一层的输出（向量）与权重矩阵（决定了线性组合系数）的乘积。

### 向量子空间

**子空间（Subspace）** 是向量空间 $V$ 的一个子集 $W$，满足：
1. 包含零向量：$\mathbf{0} \in W$
2. 对加法封闭：$\mathbf{u}, \mathbf{v} \in W \Rightarrow \mathbf{u} + \mathbf{v} \in W$
3. 对数乘封闭：$\mathbf{v} \in W, c \in \mathbb{R} \Rightarrow c\mathbf{v} \in W$

子空间的概念在降维、特征工程等机器学习任务中非常重要。例如，PCA 找到的主成分方向就构成一个低维子空间。

## 2.3 内积与投影

内积是向量之间最重要的运算之一，它建立了代数与几何的桥梁。

### 内积的定义与性质

**内积（Inner Product）**，也称为点积（Dot Product），定义为：

$$\mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^{n} u_i v_i = u_1v_1 + u_2v_2 + \cdots + u_nv_n$$

在 NumPy 中，可以使用 `np.dot()` 或 `@` 运算符计算内积：

```python
u = np.array([1, 2, 3])
v = np.array([4, 5, 6])

# 方法一：np.dot
dot_product = np.dot(u, v)

# 方法二：@ 运算符
dot_product_2 = u @ v

# 方法三：np.inner
dot_product_3 = np.inner(u, v)

print(f"内积: {dot_product}")  # 1*4 + 2*5 + 3*6 = 32
```

**内积的性质**：
1. 交换律：$\mathbf{u} \cdot \mathbf{v} = \mathbf{v} \cdot \mathbf{u}$
2. 分配律：$\mathbf{u} \cdot (\mathbf{v} + \mathbf{w}) = \mathbf{u} \cdot \mathbf{v} + \mathbf{u} \cdot \mathbf{w}$
3. 数乘结合：$(c\mathbf{u}) \cdot \mathbf{v} = c(\mathbf{u} \cdot \mathbf{v})$
4. 非负性：$\mathbf{v} \cdot \mathbf{v} \geq 0$，等号成立当且仅当 $\mathbf{v} = \mathbf{0}$

### 内积的几何解释

内积有重要的几何意义：

$$\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\| \|\mathbf{v}\| \cos\theta$$

其中 $\theta$ 是两个向量之间的夹角，$\|\cdot\|$ 表示向量的模长（L2范数）。

这个公式揭示了内积的三个用途：

**1. 计算向量夹角**

$$\cos\theta = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$

```python
def angle_between_vectors(u, v):
    """计算两个向量之间的夹角（弧度）"""
    cos_theta = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    # 防止浮点误差导致 cos_theta 超出 [-1, 1]
    cos_theta = np.clip(cos_theta, -1, 1)
    return np.arccos(cos_theta)

u = np.array([1, 0])
v = np.array([1, 1])
angle = angle_between_vectors(u, v)
print(f"夹角: {np.degrees(angle):.2f}°")  # 45°
```

**2. 判断向量关系**
- $\mathbf{u} \cdot \mathbf{v} = 0$：正交（垂直）
- $\mathbf{u} \cdot \mathbf{v} > 0$：夹角为锐角，方向相近
- $\mathbf{u} \cdot \mathbf{v} < 0$：夹角为钝角，方向相反

**3. 计算相似度（余弦相似度）**

$$\text{cosine\_similarity}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$

余弦相似度是机器学习中常用的相似度度量，广泛用于文本相似度、推荐系统等场景。

```python
from sklearn.metrics.pairwise import cosine_similarity

# 文本相似度示例
doc1 = np.array([1, 1, 0, 0])  # "机器学习"
doc2 = np.array([1, 0, 1, 0])  # "机器编程"
doc3 = np.array([0, 1, 0, 1])  # "深度学习"

docs = np.array([doc1, doc2, doc3])
similarity_matrix = cosine_similarity(docs)
print("文档相似度矩阵:\n", similarity_matrix.round(3))
```

### 柯西-施瓦茨不等式

**柯西-施瓦茨不等式（Cauchy-Schwarz Inequality）** 是内积空间中最重要的不等式：

$$|\mathbf{u} \cdot \mathbf{v}| \leq \|\mathbf{u}\| \|\mathbf{v}\|$$

等号成立当且仅当 $\mathbf{u}$ 和 $\mathbf{v}$ 线性相关。

这个不等式保证了余弦相似度的值在 $[-1, 1]$ 范围内，也保证了向量夹角的定义是有效的。

### 投影向量与正交投影

**投影（Projection）** 是内积的重要应用。向量 $\mathbf{u}$ 在向量 $\mathbf{v}$ 上的投影为：

$$\text{proj}_{\mathbf{v}} \mathbf{u} = \frac{\mathbf{u} \cdot \mathbf{v}}{\mathbf{v} \cdot \mathbf{v}} \mathbf{v} = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{v}\|^2} \mathbf{v}$$

投影将向量分解为两个正交分量：

$$\mathbf{u} = \text{proj}_{\mathbf{v}} \mathbf{u} + (\mathbf{u} - \text{proj}_{\mathbf{v}} \mathbf{u})$$

其中 $\mathbf{u} - \text{proj}_{\mathbf{v}} \mathbf{u}$ 垂直于 $\mathbf{v}$。

```python
def project(u, v):
    """计算 u 在 v 上的投影"""
    return (np.dot(u, v) / np.dot(v, v)) * v

u = np.array([3, 4])
v = np.array([1, 0])  # x 轴方向

proj = project(u, v)
perp = u - proj

print(f"原向量: {u}")
print(f"投影: {proj}")
print(f"垂直分量: {perp}")
print(f"验证正交: {np.dot(proj, perp):.6f}")  # 应该接近 0
```

### 正交基与标准正交基

**基（Basis）** 是向量空间的一组线性无关向量，使得空间中任意向量都可以表示为这组向量的线性组合。

**正交基**：基向量两两正交。

**标准正交基（Orthonormal Basis）**：正交基的每个向量都是单位向量（模长为1）。

标准正交基 $\{\mathbf{e}_1, \mathbf{e}_2, \ldots, \mathbf{e}_n\}$ 满足：

$$\mathbf{e}_i \cdot \mathbf{e}_j = \begin{cases} 1, & i = j \\ 0, & i \neq j \end{cases}$$

最常用的标准正交基是**自然基**：
- $\mathbf{e}_1 = (1, 0, 0, \ldots, 0)$
- $\mathbf{e}_2 = (0, 1, 0, \ldots, 0)$
- ...

标准正交基使得坐标计算变得简单：向量 $\mathbf{v}$ 在标准正交基下的第 $i$ 个坐标就是 $\mathbf{v} \cdot \mathbf{e}_i$。

### Gram-Schmidt 正交化过程

**Gram-Schmidt 过程** 可以将任意一组线性无关向量转化为正交基：

给定向量组 $\{\mathbf{v}_1, \mathbf{v}_2, \ldots, \mathbf{v}_n\}$：

1. $\mathbf{u}_1 = \mathbf{v}_1$
2. $\mathbf{u}_2 = \mathbf{v}_2 - \text{proj}_{\mathbf{u}_1} \mathbf{v}_2$
3. $\mathbf{u}_3 = \mathbf{v}_3 - \text{proj}_{\mathbf{u}_1} \mathbf{v}_3 - \text{proj}_{\mathbf{u}_2} \mathbf{v}_3$
4. ...

最后归一化：$\mathbf{e}_i = \frac{\mathbf{u}_i}{\|\mathbf{u}_i\|}$

```python
def gram_schmidt(vectors):
    """Gram-Schmidt 正交化"""
    basis = []
    for v in vectors:
        w = v.copy()
        for u in basis:
            w = w - project(v, u)
        if np.linalg.norm(w) > 1e-10:  # 避免零向量
            basis.append(w)
    return basis

# 示例：将两个非正交向量正交化
v1 = np.array([1.0, 1.0, 0.0])
v2 = np.array([1.0, 0.0, 1.0])

orthogonal = gram_schmidt([v1, v2])
print("正交化结果:")
for i, u in enumerate(orthogonal):
    print(f"  u{i+1} = {u}")
print(f"验证正交: u1·u2 = {np.dot(orthogonal[0], orthogonal[1]):.6f}")
```

## 2.4 向量范数

**范数（Norm）** 是衡量向量"大小"的量，可以理解为向量的"长度"。

### 范数的定义与性质

范数是一个函数 $\|\cdot\|: V \to \mathbb{R}$，满足：

1. 非负性：$\|\mathbf{v}\| \geq 0$，等号成立当且仅当 $\mathbf{v} = \mathbf{0}$
2. 齐次性：$\|c\mathbf{v}\| = |c| \|\mathbf{v}\|$
3. 三角不等式：$\|\mathbf{u} + \mathbf{v}\| \leq \|\mathbf{u}\| + \|\mathbf{v}\|$

### Lp 范数族

最常用的是 **$L_p$ 范数**，定义为：

$$\|\mathbf{v}\|_p = \left( \sum_{i=1}^{n} |v_i|^p \right)^{1/p}$$

**L2 范数（欧几里得范数）**：

$$\|\mathbf{v}\|_2 = \sqrt{\sum_{i=1}^{n} v_i^2} = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2}$$

这是我们最熟悉的"直线距离"，对应几何上从原点到向量终点的距离。

**L1 范数（曼哈顿范数）**：

$$\|\mathbf{v}\|_1 = \sum_{i=1}^{n} |v_i| = |v_1| + |v_2| + \cdots + |v_n|$$

L1 范数对应城市街区中的"曼哈顿距离"——只能沿坐标轴方向行走的总距离。

**无穷范数**：

$$\|\mathbf{v}\|_\infty = \max(|v_1|, |v_2|, \ldots, |v_n|)$$

无穷范数取向量分量绝对值的最大值。

```python
v = np.array([3, -4])

l2_norm = np.linalg.norm(v)           # L2 范数（默认）
l1_norm = np.linalg.norm(v, 1)        # L1 范数
inf_norm = np.linalg.norm(v, np.inf)  # 无穷范数

print(f"向量: {v}")
print(f"L2 范数: {l2_norm:.4f}")      # sqrt(9+16) = 5
print(f"L1 范数: {l1_norm:.4f}")      # 3+4 = 7
print(f"无穷范数: {inf_norm:.4f}")    # max(3,4) = 4
```

### 各种范数的几何意义

不同范数对应的"单位球"（范数为1的点集）形状不同：

```
L2 范数单位球:          L1 范数单位球:          L∞ 范数单位球:
    ○                      ◇                      □
   / \                    /\                    /  \
  /   \                  /  \                  |    |
 /     \                /    \                 |    |
 \     /                \    /                 |    |
  \   /                  \  /                   \  /
   \ /                    \/                      \/
    ○                      ◇                      □
```

- **L2 范数**：圆形（二维）或球面（三维），"最自然"的距离
- **L1 范数**：菱形，鼓励稀疏解
- **L∞ 范数**：正方形，关注最大分量

### 范数在正则化中的应用

在机器学习中，范数用于**正则化（Regularization）**，防止模型过拟合：

**Ridge 回归（L2 正则化）**：

$$\min_{\mathbf{w}} \left( \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \lambda \|\mathbf{w}\|_2^2 \right)$$

L2 正则化使所有参数都变小，但不会变为零。

**Lasso 回归（L1 正则化）**：

$$\min_{\mathbf{w}} \left( \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \lambda \|\mathbf{w}\|_1 \right)$$

L1 正则化会产生**稀疏解**——许多参数恰好为零，因此常用于**特征选择**。

```python
from sklearn.linear_model import Ridge, Lasso
from sklearn.datasets import make_regression

# 生成模拟数据
X, y = make_regression(n_samples=100, n_features=20, n_informative=5, random_state=42)

# Ridge 回归
ridge = Ridge(alpha=1.0)
ridge.fit(X, y)
print(f"Ridge 非零系数数量: {sum(abs(ridge.coef_) > 0.01)}")

# Lasso 回归
lasso = Lasso(alpha=0.1)
lasso.fit(X, y)
print(f"Lasso 非零系数数量: {sum(abs(lasso.coef_) > 0.01)}")
```

### 弹性网络（Elastic Net）

弹性网络结合了 L1 和 L2 正则化：

$$\min_{\mathbf{w}} \left( \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \lambda_1 \|\mathbf{w}\|_1 + \lambda_2 \|\mathbf{w}\|_2^2 \right)$$

这种方法同时享受 L1 的稀疏性和 L2 的稳定性。

---

## 本章小结

本章系统介绍了向量的核心概念：

1. **向量定义**：有序数值序列，是机器学习中数据的基本表示形式
2. **向量运算**：加法和数乘构成向量空间的基础
3. **内积与投影**：建立代数与几何的联系，用于相似度计算和正交分解
4. **向量范数**：衡量向量大小，在正则化中有重要应用

下一章将介绍矩阵——向量的自然扩展，以及线性变换的几何意义。