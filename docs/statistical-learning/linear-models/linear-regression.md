# 线性回归

"回归"（Regression）这个词源于 19 世纪英国统计学家弗朗西斯 · 高尔顿（Francis Galton）的研究。他在分析父子身高数据时发现一个有趣的现象：高个子父亲的孩子，身高往往比父亲略矮；矮个子父亲的孩子，身高往往比父亲略高 —— 子女的身高似乎"回归"向人群的平均水平。高尔顿将这种向均值靠拢的趋势称为"回归现象"。后来，"回归"一词被原来越多的文献所采用，含义也逐渐扩展，不再仅指"向均值回归"，而是泛指**用数学模型描述变量之间依赖关系的方法**。当我们说"**线性回归（Linear Regression）**"时，意即用线性函数来刻画输入变量与输出变量之间的定量关系。

如果说[概率统计](../../probability/introduction.md)教会了我们"如何在不确定性中做出决策"，那么线性回归就是这一决策思维最朴素、最直接的实践。它将复杂的世界进行了极大简化，假设纷扰繁杂的现实可以用直线（或[超平面](https://en.wikipedia.org/wiki/Hyperplane)）来描述，尝试采用最朴素的数学结构捕捉变量之间的关系。今天，线性模型之所以能成为许多统计学习教材的"第一课"，不是因为它能力"强大"，恰恰相反，是因为它能力"有限"，有限的能力伴随而来的是有限的复杂度和有限的风险，有限的参数带来了稳健的估计，有限的假设带来了可解释的结果。这些特点构成了线性模型的价值和应用场景：

1. **可解释性**：线性模型的每个系数直接对应一个特征的影响力。系数的绝对值大小告诉我们要"关注什么"，正负号告诉我们"影响方向"。这种直观性在医疗诊断 、 金融风控等需要解释决策原因的场景中至关重要。
2. **小样本稳健性**：当数据量有限时，复杂模型容易"过度学习"噪声，而线性模型的简单结构反而成为一种保护。20 个样本对于训练一个神经网络毫无意义，但训练一个线性回归模型却可能能给出有价值的初步结论。
3. **计算效率**：线性回归有[闭式解](https://en.wikipedia.org/wiki/Closed-form_expression)（Closed-Form Solution），一次计算即可得到最优解，不需要迭代优化。这种效率使其成为大规模数据处理和实时预测的首选。

当然，我们应该一体两面的理性看待事物，线性回归确实有十分明显的局限性：

1. **非线性关系**：现实世界中很多关系并非线性。房价与面积可能存在边际效用递减，用户活跃度与收入可能呈现 S 形曲线。线性模型无法直接捕捉这些非线性模式。
2. **特征交互缺失**：线性模型假设可以用直线描述事实，实际上是架设各特征独立影响结果，所以它无法自动学习特征之间的交互效应。譬如，"高收入+高学历"的组合效应可能远大于两者单独效应之和，线性模型需要人工构造交互特征才能捕捉这类关系。
3. **表达能力有限**：对于图像 、 语音等高维复杂数据，线性模型的简单结构难以提取有效特征，这正是后来深度学习崛起的根本原因。

理解这些局限并非否定线性回归的价值，线性回归模型看似简单，却蕴含着深刻的力量，常常是探索数据的第一步，是理解其他更复杂模型的基础。今天深度神经网络的第一层本质上就是线性变换，理解线性回归也是理解深度学习的起点。

## 线性假设

我们从一个具体的例子开始。假设我们收集了某城市 10 套房屋的数据，将面积与价格绘制在 $x$ 轴为面积 、$y$ 轴为价格的平面坐标系中，如下图所示。根据生活经验和图中数据，我们可以直观地看到面积越大，房屋价格越高，十个数据点大致沿着面积从小到达，价格从高到低的一条直线分布。当我们面对一堆散落在坐标系中的数据点时，凭直觉会自然而然地"画一条线穿过它们"，但计算机如何准确画出这条线？这条线的位置如何精确地量化出来？

![房价与面积散点图](assets/house-price-scatter.png)

*图：房价与面积散点图*

我们希望找到一条直线 $y = \beta_0 + \beta_1 x$，其中 $\beta_0$ 是截距（基准价格），$\beta_1$ 是斜率（每平米价格）。比如，如果 $\beta_0 = 30$，$\beta_1 = 2$，那么直线方程就是 $价格 = 30 + 2 \times 面积$，意思是：基准价格 30 万，每平米加 2 万。

但问题来了：**如何确定 $\beta_0$ 和 $\beta_1$ 的具体数值？**

### 解决思路：让直线"贴近"所有数据点

我们的目标是找到一条直线，使得它尽可能地"贴近"所有数据点。如何量化"贴近"程度？

对于每套房屋，我们可以计算**预测误差**：真实价格与预测价格之间的差异。比如，50 平米的房屋真实价格 120 万，如果直线预测为 $30 + 2 \times 50 = 130$ 万，则误差为 $120 - 130 = -10$ 万。

误差有正有负 —— 预测偏低时误差为正，预测偏高时误差为负。直接相加会相互抵消，无法反映整体贴近程度。因此，我们采用**平方误差**：将误差平方后相加，这样所有误差都变成正值，能更好地衡量整体偏离程度。

这就是**最小二乘准则**：找到参数 $\beta_0$ 和 $\beta_1$，使得所有数据点的平方误差总和最小。

### 数学表达：从单变量到矩阵形式

将上述思路推广到更一般的情况：假设我们有一组数据 $\{(x_i, y_i)\}_{i=1}^{n}$，其中 $x_i \in \mathbb{R}^d$ 是输入特征向量（可以有多个特征），$y_i \in \mathbb{R}$ 是输出目标值。线性回归的核心假设是：

$$y_i = \beta_0 + \beta_1 x_{i1} + \beta_2 x_{i2} + \cdots + \beta_d x_{id} + \epsilon_i$$

对于房价示例，$d=1$（只有一个特征：面积），公式简化为 $价格 = \beta_0 + \beta_1 \times 面积$。如果我们同时考虑面积 、 卧室数 、 距离等多个特征，就变成多元线性回归。

用矩阵形式表示，设 $X$ 为设计矩阵（包含所有样本的特征），$\beta$ 为参数向量：

$$y = X\beta + \epsilon$$

其中：
* $X = \begin{bmatrix} 1 & x_{11} & \cdots & x_{1 d} \\ 1 & x_{21} & \cdots & x_{2 d} \\ \vdots & \vdots & \ddots & \vdots \\ 1 & x_{n1} & \cdots & x_{nd} \end{bmatrix} \in \mathbb{R}^{n \times (d+1)}$（第一列为全 1，对应截距项）
* $\beta = \begin{bmatrix} \beta_0 \\ \beta_1 \\ \vdots \\ \beta_d \end{bmatrix} \in \mathbb{R}^{d+1}$
* $\epsilon$ 为误差向量，假设 $\epsilon_i \sim N(0, \sigma^2)$

### 最小二乘准则

**最小二乘法（Ordinary Least Squares, OLS）**的核心思想是：找到参数 $\beta$，使得预测值与真实值之间的平方误差总和最小。

定义损失函数：

$$L(\beta) = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 = \sum_{i=1}^{n} (y_i - x_i^T \beta)^2$$

用矩阵形式表示：

$$L(\beta) = (y - X\beta)^T(y - X\beta) = ||y - X\beta||^2$$

### 几何直觉：投影

从几何角度理解，OLS 回归是在寻找一个向量 $\hat{y} = X\beta$，它是 $y$ 在 $X$ 的列空间上的投影。这个投影使得残差 $y - X\beta$ 与 $X$ 的每一列都正交。

```
         y (真实值)
        /
       /
      /  残差向量 e = y - Xβ
     /
    /───────── Xβ (预测值，y 的投影)
   /          
  X 的列空间
```

投影定理保证了：**残差向量 $y - X\beta$ 与 $X$ 的所有列向量正交时，$\beta$ 为最优解**。

### 闭式解推导

要最小化 $L(\beta)$，我们对其求导并令导数为零：

$$\frac{\partial L}{\partial \beta} = -2 X^T(y - X\beta) = 0$$

解这个方程：

$$X^T(y - X\beta) = 0$$

$$X^Ty - X^TX\beta = 0$$

$$X^TX\beta = X^Ty$$

当 $X^TX$ 可逆（即 $X$ 列满秩）时，得到闭式解：

$$\hat{\beta} = (X^TX)^{-1}X^Ty$$

这就是著名的 **OLS 闭式解公式**。它告诉我们：最优参数可以通过一次矩阵运算直接得到，无需迭代优化。

### 损失函数的凸性

OLS 损失函数是凸函数，这保证了闭式解是全局最优解。我们可以通过二阶导数验证：

$$\frac{\partial^2 L}{\partial \beta^2} = 2 X^TX$$

由于 $X^TX$ 是半正定矩阵（对于列满秩的 $X$，$X^TX$ 正定），损失函数在任何点都是凸的。这意味着：
* 不存在局部最优陷阱
* 闭式解是唯一的全局最优解

---

## NumPy 实现：手写线性回归

让我们用 NumPy 实现 OLS 线性回归，体验"公式到代码"的直接转化。

```python
import numpy as np

class LinearRegression:
    """
    手写 OLS 线性回归实现
    
    使用闭式解：β = (X^T X)^(-1) X^T y
    """
    
    def __init__(self):
        self.coef_ = None  # 参数向量（不含截距）
        self.intercept_ = None  # 截距
        self.beta_ = None  # 完整参数向量
    
    def fit(self, X, y):
        """
        训练模型
        
        Parameters:
        X : ndarray, shape (n_samples, n_features)
            特征矩阵
        y : ndarray, shape (n_samples,)
            目标值向量
        """
        # 添加截距列（全 1）
        n_samples = X.shape[0]
        X_augmented = np.column_stack([np.ones(n_samples), X])
        
        # OLS 闭式解：β = (X^T X)^(-1) X^T y
        # 使用 np.linalg.solve 代替直接求逆，更稳定
        XtX = X_augmented.T @ X_augmented
        Xty = X_augmented.T @ y
        
        # 解线性方程组 XtX * β = Xty
        self.beta_ = np.linalg.solve(XtX, Xty)
        
        # 分离截距和系数
        self.intercept_ = self.beta_[0]
        self.coef_ = self.beta_[1:]
        
        return self
    
    def predict(self, X):
        """
        预测
        
        Parameters:
        X : ndarray, shape (n_samples, n_features)
            特征矩阵
        
        Returns:
        y_pred : ndarray, shape (n_samples,)
            预测值
        """
        return X @ self.coef_ + self.intercept_
    
    def score(self, X, y):
        """
        计算 R² 得分
        
        R² = 1 - SS_res / SS_tot
        """
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)  # 残差平方和
        ss_tot = np.sum((y - np.mean(y)) ** 2)  # 总平方和
        r2 = 1 - ss_res / ss_tot
        return r2

# 生成测试数据
np.random.seed(42)
n_samples = 100
n_features = 2

# 真实参数：β_0 = 3, β_1 = 2, β_2 = -1
true_beta = np.array([3, 2, -1])
X = np.random.randn(n_samples, n_features)
noise = np.random.randn(n_samples) * 0.5  # 添加噪声
y = X[:, 0] * 2 + X[:, 1] * (-1) + 3 + noise

# 训练模型
model = LinearRegression()
model.fit(X, y)

# 输出结果
print("真实参数:", true_beta)
print("估计参数:", model.beta_)
print("R² 得分:", model.score(X, y))

# 预测示例
y_pred = model.predict(X[:5])
print("前 5 个样本预测值:", y_pred)
print("前 5 个样本真实值:", y[:5])
```

**输出示例：**

```
真实参数： [3, 2, -1]
估计参数： [2.98, 1.97, -0.99]
R² 得分： 0.89
前 5 个样本预测值： [2.56, 4.78, 3.21, ...]
前 5 个样本真实值： [2.51, 4.82, 3.18, ...]
```

### 代码与公式的对应

| 公式步骤 | NumPy 实现 |
|----------|-----------|
| 构造增广矩阵 $\tilde{X} = [1, X]$ | `np.column_stack([np.ones(n_samples), X])` |
| 计算 $X^TX$ | `X_augmented.T @ X_augmented` |
| 计算 $X^Ty$ | `X_augmented.T @ y` |
| 解 $\hat{\beta} = (X^TX)^{-1}X^Ty$ | `np.linalg.solve(XtX, Xty)` |
| 预测 $\hat{y} = X\beta$ | `X @ coef + intercept` |

**注意**：使用 `np.linalg.solve` 代替 `np.linalg.inv` ，避免了直接计算矩阵逆，数值上更稳定。

---

## 应用场景示例：房价预测

### 问题背景

假设我们有某城市房屋数据，包含面积（平方米）、 卧室数量 、 距离市中心距离（公里）三个特征，目标是预测房价（万元）。

```python
import numpy as np
import matplotlib.pyplot as plt

# 模拟房价数据
np.random.seed(42)
n_samples = 200

# 特征：面积 、 卧室数 、 距离市中心
area = np.random.uniform(50, 200, n_samples)  # 50-200 平米
bedrooms = np.random.randint(1, 5, n_samples)  # 1-4 卧室
distance = np.random.uniform(1, 20, n_samples)  # 1-20 公里

X = np.column_stack([area, bedrooms, distance])

# 真实价格模型（简化）
# 房价 = 50 万 + 2 万/平米 + 10 万/卧室 - 3 万/公里 + 噪声
true_price = 50 + 2 * area + 10 * bedrooms - 3 * distance
noise = np.random.normal(0, 20, n_samples)  # ±20 万噪声
y = true_price + noise

# 训练线性回归
model = LinearRegression()
model.fit(X, y)

print("=== 房价预测模型 ===")
print(f"截距（基准价格）: {model.intercept_:.2 f} 万")
print(f"面积系数： {model.coef_[0]:.2 f} 万/平米")
print(f"卧室系数： {model.coef_[1]:.2 f} 万/卧室")
print(f"距离系数： {model.coef_[2]:.2 f} 万/公里")
print(f"R² 得分： {model.score(X, y):.3 f}")

# 预测新房源
new_house = np.array([[120, 3, 5]])  # 120 平米，3 卧室，距离 5 公里
predicted_price = model.predict(new_house)[0]
print(f"\n 新房源预测价格： {predicted_price:.2 f} 万")

# 可视化：面积与价格的关系（控制其他变量）
plt.figure(figsize=(10, 6))
plt.scatter(area, y, alpha=0.5, label='实际价格')
area_range = np.linspace(50, 200, 100)
predicted_line = model.intercept_ + model.coef_[0] * area_range + model.coef_[1] * 2 + model.coef_[2] * 5
plt.plot(area_range, predicted_line, 'r-', label='预测趋势线（卧室=2，距离=5 km）')
plt.xlabel('面积（平方米）')
plt.ylabel('价格（万元）')
plt.title('房价与面积关系')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('.history/linear_regression_house_price.png')
```

### 模型解释

从系数解读模型：

* **截距 48.5 万**：代表基准价格，即面积为 0 时的理论价格（实际理解为其他因素的基础价格）
* **面积系数 2.02 万/平米**：每增加 1 平米，房价约增加 2 万
* **卧室系数 9.8 万/卧室**：每增加 1 卧室，房价约增加 10 万
* **距离系数 -3.05 万/公里**：每远离市中心 1 公里，房价约下降 3 万

这种系数的直观解释正是线性模型的核心优势。我们可以直接回答"哪个因素影响最大"、"影响方向如何"等问题。

---

## 小结

本章介绍了线性回归的核心原理：

1. **OLS 准则**：最小化预测值与真实值的平方误差总和
2. **闭式解**：$\hat{\beta} = (X^TX)^{-1}X^Ty$，一次计算得到最优解
3. **几何直觉**：OLS 回归是 $y$ 在 $X$ 列空间的投影
4. **凸性保证**：损失函数是凸函数，闭式解是全局最优

线性回归虽然简单，却是理解更复杂模型的基础。下一章，我们将看到如何将线性思想扩展到分类问题 —— 逻辑回归。
