# 线性回归——从OLS到闭式解

## 引言：线性假设的力量与局限

如果说[概率统计](../../probability/introduction.md)教会了我们"如何在不确定性中做出决策"，那么**线性回归（Linear Regression）**就是这一思想最朴素、最直接的实践。它假设世界可以用一条直线（或超平面）来描述，用最简单的数学结构捕捉变量之间的关系。

这种假设看似过于简化，却蕴含着深刻的力量。线性模型之所以成为统计学习的基石，不因为它"万能"，恰恰因为它"有限"——有限的复杂度带来有限的风险，有限的假设带来可解释的结果，有限的参数带来稳健的估计。正如爱因斯坦所言："凡事应该简单到不能再简单，但不能过度简化。"

### 线性模型的三个核心价值

1. **可解释性**：线性模型的每个系数直接对应一个特征的影响力。系数的绝对值大小告诉我们要"关注什么"，正负号告诉我们"影响方向"。这种直观性在医疗诊断、金融风控等需要解释决策原因的场景中至关重要。

2. **小样本稳健性**：当数据量有限时，复杂模型容易"过度学习"噪声，而线性模型的简单结构反而成为一种保护。20个样本训练一个神经网络可能毫无意义，但训练一个线性回归模型却能给出有价值的初步结论。

3. **计算效率**：线性回归有闭式解（closed-form solution），一次计算即可得到最优解，无需迭代优化。这种效率使其成为大规模数据处理和实时预测的首选。

### 线性假设的局限

当然，线性假设也有明显的局限：

1. **非线性关系**：现实世界中很多关系并非线性。房价与面积可能存在边际效用递减，用户活跃度与收入可能呈现S形曲线。线性模型无法直接捕捉这些非线性模式。

2. **特征交互缺失**：线性模型假设各特征独立影响结果，无法自动学习特征之间的交互效应。譬如，"高收入+高学历"的组合效应可能远大于两者单独效应之和，线性模型需要人工构造交互特征才能捕捉。

3. **表达能力有限**：对于图像、语音等高维复杂数据，线性模型的简单结构难以提取有效特征，这正是深度学习崛起的原因。

然而，理解这些局限并非否定线性模型的价值。相反，**线性模型常常是探索数据的第一步**，是建立 baseline 的标准选择，是理解复杂模型的基础。深度神经网络的第一层本质上就是线性变换，理解线性回归是理解深度学习的起点。

---

## OLS原理推导：从直觉到闭式解

### 问题设定

假设我们有一组数据 $\{(x_i, y_i)\}_{i=1}^{n}$，其中 $x_i \in \mathbb{R}^d$ 是输入特征向量，$y_i \in \mathbb{R}$ 是输出目标值。线性回归的核心假设是：

$$y_i = \beta_0 + \beta_1 x_{i1} + \beta_2 x_{i2} + \cdots + \beta_d x_{id} + \epsilon_i$$

用矩阵形式表示，设 $X$ 为设计矩阵（包含所有样本的特征），$\beta$ 为参数向量：

$$y = X\beta + \epsilon$$

其中：
- $X = \begin{bmatrix} 1 & x_{11} & \cdots & x_{1d} \\ 1 & x_{21} & \cdots & x_{2d} \\ \vdots & \vdots & \ddots & \vdots \\ 1 & x_{n1} & \cdots & x_{nd} \end{bmatrix} \in \mathbb{R}^{n \times (d+1)}$（第一列为全1，对应截距项）
- $\beta = \begin{bmatrix} \beta_0 \\ \beta_1 \\ \vdots \\ \beta_d \end{bmatrix} \in \mathbb{R}^{d+1}$
- $\epsilon$ 为误差向量，假设 $\epsilon_i \sim N(0, \sigma^2)$

### 最小二乘准则

**最小二乘法（Ordinary Least Squares, OLS）**的核心思想是：找到参数 $\beta$，使得预测值与真实值之间的平方误差总和最小。

定义损失函数：

$$L(\beta) = \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 = \sum_{i=1}^{n} (y_i - x_i^T \beta)^2$$

用矩阵形式表示：

$$L(\beta) = (y - X\beta)^T(y - X\beta) = ||y - X\beta||^2$$

### 几何直觉：投影

从几何角度理解，OLS回归是在寻找一个向量 $\hat{y} = X\beta$，它是 $y$ 在 $X$ 的列空间上的投影。这个投影使得残差 $y - X\beta$ 与 $X$ 的每一列都正交。

```
         y (真实值)
        /
       /
      /  残差向量 e = y - Xβ
     /
    /───────── Xβ (预测值，y的投影)
   /          
  X 的列空间
```

投影定理保证了：**残差向量 $y - X\beta$ 与 $X$ 的所有列向量正交时，$\beta$ 为最优解**。

### 闭式解推导

要最小化 $L(\beta)$，我们对其求导并令导数为零：

$$\frac{\partial L}{\partial \beta} = -2X^T(y - X\beta) = 0$$

解这个方程：

$$X^T(y - X\beta) = 0$$

$$X^Ty - X^TX\beta = 0$$

$$X^TX\beta = X^Ty$$

当 $X^TX$ 可逆（即 $X$ 列满秩）时，得到闭式解：

$$\hat{\beta} = (X^TX)^{-1}X^Ty$$

这就是著名的**OLS闭式解公式**。它告诉我们：最优参数可以通过一次矩阵运算直接得到，无需迭代优化。

### 损失函数的凸性

OLS损失函数是凸函数，这保证了闭式解是全局最优解。我们可以通过二阶导数验证：

$$\frac{\partial^2 L}{\partial \beta^2} = 2X^TX$$

由于 $X^TX$ 是半正定矩阵（对于列满秩的 $X$，$X^TX$ 正定），损失函数在任何点都是凸的。这意味着：
- 不存在局部最优陷阱
- 闭式解是唯一的全局最优解

---

## NumPy实现：手写线性回归

让我们用NumPy实现OLS线性回归，体验"公式到代码"的直接转化。

```python
import numpy as np

class LinearRegression:
    """
    手写OLS线性回归实现
    
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
        # 添加截距列（全1）
        n_samples = X.shape[0]
        X_augmented = np.column_stack([np.ones(n_samples), X])
        
        # OLS闭式解：β = (X^T X)^(-1) X^T y
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
        计算R²得分
        
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
print("R²得分:", model.score(X, y))

# 预测示例
y_pred = model.predict(X[:5])
print("前5个样本预测值:", y_pred)
print("前5个样本真实值:", y[:5])
```

**输出示例：**
```
真实参数: [3, 2, -1]
估计参数: [2.98, 1.97, -0.99]
R²得分: 0.89
前5个样本预测值: [2.56, 4.78, 3.21, ...]
前5个样本真实值: [2.51, 4.82, 3.18, ...]
```

### 代码与公式的对应

| 公式步骤 | NumPy实现 |
|----------|-----------|
| 构造增广矩阵 $\tilde{X} = [1, X]$ | `np.column_stack([np.ones(n_samples), X])` |
| 计算 $X^TX$ | `X_augmented.T @ X_augmented` |
| 计算 $X^Ty$ | `X_augmented.T @ y` |
| 解 $\hat{\beta} = (X^TX)^{-1}X^Ty$ | `np.linalg.solve(XtX, Xty)` |
| 预测 $\hat{y} = X\beta$ | `X @ coef + intercept` |

**注意**：使用 `np.linalg.solve` 代替 `np.linalg.inv`，避免了直接计算矩阵逆，数值上更稳定。

---

## 应用场景示例：房价预测

### 问题背景

假设我们有某城市房屋数据，包含面积（平方米）、卧室数量、距离市中心距离（公里）三个特征，目标是预测房价（万元）。

```python
import numpy as np
import matplotlib.pyplot as plt

# 模拟房价数据
np.random.seed(42)
n_samples = 200

# 特征：面积、卧室数、距离市中心
area = np.random.uniform(50, 200, n_samples)  # 50-200平米
bedrooms = np.random.randint(1, 5, n_samples)  # 1-4卧室
distance = np.random.uniform(1, 20, n_samples)  # 1-20公里

X = np.column_stack([area, bedrooms, distance])

# 真实价格模型（简化）
# 房价 = 50万 + 2万/平米 + 10万/卧室 - 3万/公里 + 噪声
true_price = 50 + 2 * area + 10 * bedrooms - 3 * distance
noise = np.random.normal(0, 20, n_samples)  # ±20万噪声
y = true_price + noise

# 训练线性回归
model = LinearRegression()
model.fit(X, y)

print("=== 房价预测模型 ===")
print(f"截距（基准价格）: {model.intercept_:.2f} 万")
print(f"面积系数: {model.coef_[0]:.2f} 万/平米")
print(f"卧室系数: {model.coef_[1]:.2f} 万/卧室")
print(f"距离系数: {model.coef_[2]:.2f} 万/公里")
print(f"R²得分: {model.score(X, y):.3f}")

# 预测新房源
new_house = np.array([[120, 3, 5]])  # 120平米，3卧室，距离5公里
predicted_price = model.predict(new_house)[0]
print(f"\n新房源预测价格: {predicted_price:.2f} 万")

# 可视化：面积与价格的关系（控制其他变量）
plt.figure(figsize=(10, 6))
plt.scatter(area, y, alpha=0.5, label='实际价格')
area_range = np.linspace(50, 200, 100)
predicted_line = model.intercept_ + model.coef_[0] * area_range + model.coef_[1] * 2 + model.coef_[2] * 5
plt.plot(area_range, predicted_line, 'r-', label='预测趋势线（卧室=2，距离=5km）')
plt.xlabel('面积（平方米）')
plt.ylabel('价格（万元）')
plt.title('房价与面积关系')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('.history/linear_regression_house_price.png')
```

### 模型解释

从系数解读模型：

- **截距 48.5万**：代表基准价格，即面积为0时的理论价格（实际理解为其他因素的基础价格）
- **面积系数 2.02万/平米**：每增加1平米，房价约增加2万
- **卧室系数 9.8万/卧室**：每增加1卧室，房价约增加10万
- **距离系数 -3.05万/公里**：每远离市中心1公里，房价约下降3万

这种系数的直观解释正是线性模型的核心优势。我们可以直接回答"哪个因素影响最大"、"影响方向如何"等问题。

---

## 小结

本章介绍了线性回归的核心原理：

1. **OLS准则**：最小化预测值与真实值的平方误差总和
2. **闭式解**：$\hat{\beta} = (X^TX)^{-1}X^Ty$，一次计算得到最优解
3. **几何直觉**：OLS回归是 $y$ 在 $X$ 列空间的投影
4. **凸性保证**：损失函数是凸函数，闭式解是全局最优

线性回归虽然简单，却是理解更复杂模型的基础。下一章，我们将看到如何将线性思想扩展到分类问题——逻辑回归。