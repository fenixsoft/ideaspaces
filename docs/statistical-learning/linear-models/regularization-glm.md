# 正则化与广义线性模型

## 引言：从拟合到泛化

前两章我们学习了线性回归和逻辑回归，掌握了从数据中拟合模型参数的方法。然而，机器学习的核心目标不是"拟合训练数据"，而是"泛化到未见数据"——在训练集上表现完美，在新数据上预测失败，这是机器学习最常见的陷阱：**过拟合（Overfitting）**。

正则化（Regularization）正是应对过拟合的核心技术。它通过在损失函数中加入参数约束，限制模型的复杂度，强迫模型"简约而非完美"。正如统计学家George Box的名言："所有模型都是错的，但有些是有用的。"正则化帮助我们找到"有用的简单模型"，而非"无用的复杂模型"。

---

## 过拟合：模型学习的陷阱

### 过拟合现象

假设我们要拟合一条曲线。训练数据有10个点：

```
真实关系: y = sin(x) + 噪声

模型选择:
1. 线性模型 (y = ax + b): 欠拟合，误差大
2. 9次多项式 (y = a₀ + a₁x + ... + a₉x⁹): 过拟合，误差小但泛化差
3. 3次多项式: 适中，泛化好
```

9次多项式可以在训练数据上达到完美拟合（误差为0），但它的复杂曲线在新数据上往往预测错误。这种"过度学习训练数据"的现象就是过拟合。

### 过拟合的成因

过拟合的产生源于三个因素：

1. **模型复杂度过高**：参数数量过多，模型有足够的"自由度"去拟合噪声而非真实规律
2. **训练数据不足**：样本数量太少，模型无法学到真实的统计规律
3. **噪声干扰**：训练数据中的噪声被模型当作规律学习

**根本原因**：模型从"有限样本"学习，却试图推断"无限未见数据"的规律。当模型复杂度超过数据所能支撑的程度，就会产生过拟合。

### 过拟合识别方法

如何判断模型是否过拟合？核心方法是**比较训练误差和验证误差**：

```python
# 过拟合诊断示例
train_error = 0.02  # 训练误差很小
val_error = 0.35    # 验证误差很大

if val_error >> train_error:
    print("过拟合!")
elif val_error ≈ train_error and both large:
    print("欠拟合!")
else:
    print("拟合适中!")
```

---

## 正则化原理：约束参数防过拟合

### 核心思想

正则化通过在损失函数中加入**参数惩罚项**，限制参数的大小：

$$L_{reg}(\beta) = L(\beta) + \lambda \cdot R(\beta)$$

其中：
- $L(\beta)$：原损失函数（如OLS的平方损失）
- $R(\beta)$：正则化项，惩罚参数大小
- $\lambda$：正则化强度，控制惩罚程度

### 为什么约束参数有效？

参数值过大意味着模型对输入特征"过度敏感"——微小的输入变化会导致巨大的输出变化。这种敏感性正是过拟合的特征。

通过约束参数：
1. 模型输出变化更平滑，对新数据更稳定
2. 某些参数可能被压缩到0，自动进行"特征选择"
3. 模型复杂度被限制，降低过拟合风险

---

## 岭回归（L2正则化）

### 数学推导

**岭回归（Ridge Regression）**在OLS损失中加入L2正则化项：

$$L_{Ridge}(\beta) = ||y - X\beta||^2 + \lambda ||\beta||^2_2$$

其中 $||\beta||^2_2 = \sum_{j=1}^{d} \beta_j^2$ 是参数的L2范数平方。

求解最小值，对 $\beta$ 求导：

$$\frac{\partial L}{\partial \beta} = -2X^T(y - X\beta) + 2\lambda\beta = 0$$

整理得：

$$X^TX\beta + \lambda\beta = X^Ty$$

$$\hat{\beta}_{Ridge} = (X^TX + \lambda I)^{-1}X^Ty$$

与OLS闭式解 $\hat{\beta}_{OLS} = (X^TX)^{-1}X^Ty$ 对比，岭回归在 $X^TX$ 上加了 $\lambda I$。

### 关键特性

1. **始终有解**：当 $X^TX$ 不可逆（如特征共线性）时，OLS无解，但岭回归加上 $\lambda I$ 后矩阵一定可逆
2. **参数收缩**：正则化项 $\lambda\beta$ 使得参数估计值比OLS小，但不会精确为0
3. **处理共线性**：当多个特征高度相关时，岭回归能稳定估计参数

### NumPy实现

```python
import numpy as np

class RidgeRegression:
    """
    岭回归实现（L2正则化）
    """
    
    def __init__(self, alpha=1.0):
        self.alpha = alpha  # 正则化强度λ
        self.coef_ = None
        self.intercept_ = None
    
    def fit(self, X, y):
        """训练模型"""
        n_samples = X.shape[0]
        X_augmented = np.column_stack([np.ones(n_samples), X])
        
        # 岭回归闭式解：β = (X^T X + λI)^(-1) X^T y
        # 注意：不对截距项正则化（I的第一行第一列为0）
        I = np.eye(X_augmented.shape[1])
        I[0, 0] = 0  # 截距项不正则化
        
        XtX = X_augmented.T @ X_augmented
        Xty = X_augmented.T @ y
        
        self.beta_ = np.linalg.solve(XtX + self.alpha * I, Xty)
        
        self.intercept_ = self.beta_[0]
        self.coef_ = self.beta_[1:]
        
        return self
    
    def predict(self, X):
        """预测"""
        return X @ self.coef_ + self.intercept_
    
    def score(self, X, y):
        """R²得分"""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - ss_res / ss_tot


# 演示：共线性问题
np.random.seed(42)
n_samples = 50

# 生成高度相关的特征
x1 = np.random.randn(n_samples)
x2 = x1 + np.random.randn(n_samples) * 0.01  # x2几乎等于x1（共线性）
x3 = np.random.randn(n_samples)
X = np.column_stack([x1, x2, x3])

# 目标值
y = 2 * x1 + 3 * x3 + np.random.randn(n_samples) * 0.5

# OLS尝试（可能不稳定）
try:
    from numpy.linalg import LinAlgError
    XtX = np.column_stack([np.ones(n_samples), X]).T @ np.column_stack([np.ones(n_samples), X])
    beta_ols = np.linalg.solve(XtX, np.column_stack([np.ones(n_samples), X]).T @ y)
    print("OLS参数:", beta_ols[1:])  # 可能数值不稳定
except LinAlgError:
    print("OLS: 矩阵不可逆!")

# 岭回归
ridge = RidgeRegression(alpha=1.0)
ridge.fit(X, y)
print(f"岭回归参数: {ridge.coef_}")
print(f"岭回归R²: {ridge.score(X, y):.3f}")
```

### λ参数选择

正则化强度 $\lambda$ 的选择至关重要：
- $\lambda = 0$：退化为OLS，可能过拟合
- $\lambda$ 太小：正则化效果不明显
- $\lambda$ 太大：参数过度收缩，可能欠拟合
- $\lambda$适中：平衡拟合与泛化

实践中常用**交叉验证**选择最优 $\lambda$。

---

## Lasso（L1正则化）

### 数学定义

**Lasso（Least Absolute Shrinkage and Selection Operator）**使用L1正则化：

$$L_{Lasso}(\beta) = ||y - X\beta||^2 + \lambda ||\beta||_1$$

其中 $||\beta||_1 = \sum_{j=1}^{d} |\beta_j|$ 是参数的L1范数。

### 稀疏性：Lasso的核心优势

Lasso最独特的特性是**产生稀疏解**——某些参数精确为0。这带来两个好处：

1. **自动特征选择**：系数为0的特征相当于被"剔除"，Lasso自动选择最重要的特征
2. **模型简洁**：稀疏模型更容易解释，计算更快

### 为什么L1产生稀疏解？

几何直觉：L1范数的约束区域是"菱形"，L2是"圆形"。损失函数等高线与约束区域相交时，L1更容易在"顶点"（即某个坐标轴）处相交，意味着某个参数为0。

```
L2约束（圆形）:          L1约束（菱形）:
    β₂                     β₂
    ↑                      ↑
    │    ○                 │   ◇
    │  ○ ○                 │ ◇ ◇
    │○ ○ ○                 │◇ ◇ ◇
────┼───────→ β₁      ────┼──◇───→ β₁
    │○ ○ ○                 │◇ ◇ ◇
    │  ○ ○                 │ ◇ ◇
    │    ○                 │   ◇

等高线与约束相交:
L2: 相交点参数都非零
L1: 相交点可能在顶点，某参数=0
```

### NumPy实现：坐标下降法

Lasso没有闭式解，需要迭代优化。**坐标下降法（Coordinate Descent）**是常用算法：每次只更新一个参数，其他参数固定。

```python
class LassoRegression:
    """
    Lasso回归实现（L1正则化）
    使用坐标下降算法
    """
    
    def __init__(self, alpha=1.0, n_iterations=1000):
        self.alpha = alpha
        self.n_iterations = n_iterations
        self.coef_ = None
        self.intercept_ = None
    
    def soft_threshold(self, rho, lambda_):
        """软阈值函数"""
        if rho < -lambda_:
            return rho + lambda_
        elif rho > lambda_:
            return rho - lambda_
        else:
            return 0
    
    def fit(self, X, y):
        """训练模型（坐标下降）"""
        n_samples, n_features = X.shape
        
        # 初始化参数
        self.coef_ = np.zeros(n_features)
        self.intercept_ = np.mean(y)
        
        # 数据标准化（加速收敛）
        X_centered = X - np.mean(X, axis=0)
        y_centered = y - self.intercept
        
        # 坐标下降迭代
        for iteration in range(self.n_iterations):
            for j in range(n_features):
                # 计算rho（未正则化的梯度项）
                residual = y_centered - X_centered @ self.coef_ + self.coef_[j] * X_centered[:, j]
                rho = X_centered[:, j] @ residual / n_samples
                
                # 应用软阈值
                self.coef_[j] = self.soft_threshold(rho, self.alpha)
        
        return self
    
    def predict(self, X):
        """预测"""
        return X @ self.coef_ + self.intercept
    
    def score(self, X, y):
        """R²得分"""
        y_pred = self.predict(X)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - ss_res / ss_tot


# 演示Lasso的稀疏性
np.random.seed(42)
n_samples = 100
n_features = 10

# 生成数据：只有3个特征真正有用
X = np.random.randn(n_samples, n_features)
true_coef = np.array([5, 3, -2, 0, 0, 0, 0, 0, 0, 0])  # 只有前3个有效
y = X @ true_coef + np.random.randn(n_samples) * 0.5

# Lasso回归
lasso = LassoRegression(alpha=0.5, n_iterations=1000)
lasso.fit(X, y)

print("=== Lasso稀疏性演示 ===")
print("真实系数:", true_coef)
print("Lasso估计:", lasso.coef_)
print(f"R²得分: {lasso.score(X, y):.3f}")
print(f"非零参数数量: {np.sum(np.abs(lasso.coef_) > 0.01)} (原始{len(true_coef)}个)")
```

---

## L1与L2正则化对比

| 特性 | L2正则化（岭回归） | L1正则化（Lasso） |
|------|-------------------|-------------------|
| 参数约束 | 收缩但不为零 | 可精确为零（稀疏） |
| 特征选择 | 不自动选择 | 自动选择 |
| 计算复杂度 | 有闭式解，计算快 | 需迭代优化 |
| 共线性处理 | 稳定处理 | 参数不稳定 |
| 适用场景 | 特征都相关时 | 特征筛选时 |

### Elastic Net：两者结合

当特征之间存在相关性且需要稀疏解时，可以使用**Elastic Net**：

$$L_{EN}(\beta) = ||y - X\beta||^2 + \lambda_1 ||\beta||_1 + \lambda_2 ||\beta||_2^2$$

结合L1的稀疏性和L2的稳定性。

---

## GLM框架：统一视角

### 广义线性模型定义

**广义线性模型（Generalized Linear Model, GLM）**统一了线性回归、逻辑回归等模型：

$$y = g^{-1}(X\beta)$$

其中：
- $g$：**连接函数（Link Function）**，连接线性预测与响应变量
- $y$：响应变量，服从某种指数分布族

### 三要素

1. **分布族**：响应变量 $y$ 服从的分布（正态分布、伯努利分布、泊松分布等）
2. **线性预测器**：$X\beta$，线性组合输入特征
3. **连接函数**：$g$，连接线性预测器与分布均值

### 常见GLM实例

| 模型 | 分布族 | 连接函数 | 典型应用 |
|------|--------|----------|----------|
| 线性回归 | 正态分布 | $g(\mu) = \mu$（identity） | 连续值预测 |
| 逻辑回归 | 伯努利分布 | $g(\mu) = \log\frac{\mu}{1-\mu}$（logit） | 二分类 |
| Poisson回归 | 泊松分布 | $g(\mu) = \log\mu$（log） | 计数预测 |
| Probit回归 | 正态分布 | $g(\mu) = \Phi^{-1}(\mu)$（probit） | 二分类 |

### GLM的意义

GLM框架告诉我们：**线性回归和逻辑回归本质上是同一种模型，只是连接函数和分布假设不同**。

- 线性回归：假设 $y$ 服从正态分布，直接预测均值
- 逻辑回归：假设 $y$ 服从伯努利分布，通过logit连接函数预测概率

这种统一视角帮助我们理解：
1. 不同模型的数学本质是一致的
2. 选择模型的关键是理解数据分布特性
3. 可以根据问题性质选择合适的连接函数和分布族

---

## 与深度学习的对比

### 线性模型在深度时代的价值

尽管深度学习在很多领域超越传统方法，线性模型依然有其独特价值：

**1. 可解释性优势**

深度神经网络是"黑箱"，难以解释为什么做出某个预测。线性模型的系数直接告诉我们每个特征的影响方向和程度。在医疗诊断、金融风控、法律判决等需要解释决策的场景，线性模型是首选。

```python
# 线性模型解释示例
print("房价预测模型解读:")
print("- 每平米增加2万元价格")
print("- 每卧室增加10万元价格")
print("- 每远离市中心1公里减少3万元")
# 这对用户和监管者都有意义
```

**2. 小样本场景**

当数据量很少（几十到几百样本）时，深度学习无法发挥作用。线性模型反而因其简单结构而稳健——复杂模型会过拟合，简单模型反而能学到有用规律。

**3. Baseline标准**

在探索新问题时，线性模型是建立baseline的标准选择。如果线性模型能解决问题，就没有必要用复杂模型；如果线性模型效果差，再考虑更复杂的方法。

**4. 计算效率**

线性回归有闭式解，一次计算得到最优参数，无需GPU训练。对于实时预测、大规模数据处理场景，线性模型效率远超深度学习。

**5. 特征工程基础**

深度学习的"自动特征学习"依赖于海量数据和复杂架构。当数据有限或问题结构简单时，手工特征工程+线性模型往往效果更好。

### 线性模型的局限

当然，线性模型有明显局限：

1. **非线性关系**：无法直接捕捉非线性模式，需要手工构造非线性特征
2. **特征交互**：需要人工设计交互特征，无法自动学习
3. **高维复杂数据**：图像、语音、自然语言等复杂数据，线性模型难以提取有效特征

### 深度学习与线性模型的关系

有趣的是，**深度神经网络本质上是多个线性变换的非线性组合**：

- 每一层：$z = Wx + b$（线性变换）
- 激活函数：$a = \sigma(z)$（非线性映射）

理解线性回归是理解神经网络的第一步。神经网络的权重矩阵 $W$ 本质上就是线性回归参数 $\beta$ 的扩展。

---

## 小结

本章介绍了正则化和GLM框架：

1. **过拟合风险**：模型复杂度过高、数据不足、噪声干扰导致过拟合
2. **正则化原理**：通过参数约束限制模型复杂度
3. **岭回归（L2）**：参数收缩，处理共线性，始终有解
4. **Lasso（L1）**：产生稀疏解，自动特征选择
5. **GLM框架**：统一视角看待线性回归和逻辑回归

线性模型是机器学习的基石。它们简单但不简陋，有限但有用。理解线性模型，是理解复杂模型的基础；掌握正则化，是防止过拟合的核心技能。