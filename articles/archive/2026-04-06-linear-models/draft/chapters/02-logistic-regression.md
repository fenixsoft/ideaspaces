# 逻辑回归——分类问题的概率解法

## 引言：从回归到分类

线性回归解决的是"预测数值"的问题——房价是多少？销量是多少？这些问题输出连续的数值。然而，现实中大量问题需要回答的是"判断类别"：邮件是不是垃圾邮件？客户会不会流失？图片中有没有猫？

这类**分类问题（Classification）**的输出是离散的类别标签，而不是连续数值。我们能否直接用线性回归来解决分类问题？

### 线性回归用于分类的问题

假设我们用线性回归来做二分类（标签为0或1）。模型输出 $y = X\beta$ 可能是任意实数，我们设置阈值：当 $y \geq 0.5$ 时预测为类别1，否则预测为类别0。

这种方法存在几个问题：

1. **输出无界**：线性回归输出可以是任意值，如 $y = -10$ 或 $y = 100$，这无法解释为"概率"
2. **损失函数不合理**：当真实标签为1，模型输出100时，损失函数反而会惩罚这个"正确预测"，因为它偏离了"理想输出1"
3. **对异常值敏感**：少数极端值会显著影响模型参数

**逻辑回归（Logistic Regression）**正是为解决这些问题而设计。它通过一个关键变换——**Sigmoid函数**——将线性输出映射到(0,1)区间，使其可以解释为概率。

---

## Sigmoid函数：连接线性与概率

### 数学定义

Sigmoid函数（也称Logistic函数）定义为：

$$\sigma(z) = \frac{1}{1 + e^{-z}} = \frac{e^z}{1 + e^z}$$

其图像是一条S形曲线：

```
σ(z)
1 ┤        ___________
  │       /
  │      /
0.5┤─────/──────────────
  │    /
  │   /
0 ┤__/________________
    -6  -2  0  2  6    z
```

### 关键性质

1. **值域(0,1)**：输出严格限制在0到1之间，可以解释为概率
2. **单调递增**：输入越大，输出越接近1
3. **中心点σ(0)=0.5**：当输入为0时，输出为0.5，表示"不确定"
4. **导数简洁**：$\sigma'(z) = \sigma(z)(1-\sigma(z))$，这一性质在梯度计算中极为重要

### NumPy实现与可视化

```python
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(z):
    """Sigmoid函数"""
    return 1 / (1 + np.exp(-z))

# 可视化
z = np.linspace(-10, 10, 100)
sigma_z = sigmoid(z)

plt.figure(figsize=(10, 6))
plt.plot(z, sigma_z, 'b-', label='σ(z)')
plt.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
plt.axvline(0, color='gray', linestyle='--', alpha=0.5)
plt.xlabel('z')
plt.ylabel('σ(z)')
plt.title('Sigmoid函数')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('.history/sigmoid_function.png')

# 演示性质
print("σ(-5) =", sigmoid(-5))  # ≈ 0.0067
print("σ(0) =", sigmoid(0))    # = 0.5
print("σ(5) =", sigmoid(5))    # ≈ 0.9933

# 导数验证
z_test = 2.0
sigma_val = sigmoid(z_test)
sigma_derivative = sigma_val * (1 - sigma_val)
print(f"σ(2) = {sigma_val:.4f}, σ'(2) = {sigma_derivative:.4f}")
```

### 概率解释

为什么Sigmoid输出可以解释为概率？这源于其与**log odds**的关系。

设事件发生概率为 $p$，**odds**定义为 $p/(1-p)$（发生与不发生概率之比）。**log odds（对数几率）**为：

$$\log\frac{p}{1-p} = z$$

反解 $p$：

$$p = \frac{e^z}{1+e^z} = \sigma(z)$$

这说明：**Sigmoid函数将"对数几率"映射为概率**。如果线性模型输出 $z = X\beta$ 表示对数几率，那么 $\sigma(X\beta)$ 就是事件发生的概率。

---

## 交叉熵损失：从最大似然推导

### 为什么不用平方损失？

如果我们用平方损失 $L = (y - \hat{p})^2$，其中 $\hat{p} = \sigma(X\beta)$，会遇到问题：

1. **非凸性**：引入Sigmoid后，平方损失变成非凸函数，可能存在多个局部最优
2. **梯度消失**：当 $\sigma(z)$ 接近0或1时，梯度 $\sigma'(z)$ 接近0，学习速度极慢

### 最大似然估计

假设样本标签 $y_i$ 来自伯努利分布：$P(y_i=1) = p_i = \sigma(X_i\beta)$，$P(y_i=0) = 1-p_i$。

单个样本的似然：

$$L_i = p_i^{y_i}(1-p_i)^{1-y_i}$$

所有样本的似然：

$$L(\beta) = \prod_{i=1}^{n} p_i^{y_i}(1-p_i)^{1-y_i}$$

取对数（将乘法转为加法）：

$$\log L(\beta) = \sum_{i=1}^{n} [y_i \log p_i + (1-y_i)\log(1-p_i)]$$

最大化似然等价于最小化**交叉熵损失（Cross-Entropy Loss）**：

$$J(\beta) = -\frac{1}{n}\sum_{i=1}^{n} [y_i \log p_i + (1-y_i)\log(1-p_i)]$$

其中 $p_i = \sigma(X_i\beta)$。

### 梯度推导

损失函数对参数 $\beta$ 的梯度：

$$\frac{\partial J}{\partial \beta} = \frac{1}{n}\sum_{i=1}^{n} (p_i - y_i) X_i$$

用矩阵形式表示：

$$\nabla_\beta J = \frac{1}{n}X^T(\hat{p} - y)$$

这一简洁的梯度公式使得逻辑回归可以用梯度下降高效优化。

**关键洞察**：梯度 $(p_i - y_i)$ 表示"预测概率与真实标签的偏差"。当预测准确时，梯度接近0，参数不再调整；当预测错误时，梯度驱动参数朝正确方向移动。

---

## NumPy实现：手写逻辑回归

```python
import numpy as np

class LogisticRegression:
    """
    手写逻辑回归实现
    
    使用梯度下降优化交叉熵损失
    """
    
    def __init__(self, learning_rate=0.1, n_iterations=1000):
        self.lr = learning_rate
        self.n_iterations = n_iterations
        self.coef_ = None
        self.intercept_ = None
        self.loss_history = []
    
    def sigmoid(self, z):
        """Sigmoid函数"""
        # 防止数值溢出
        z = np.clip(z, -500, 500)
        return 1 / (1 + np.exp(-z))
    
    def cross_entropy_loss(self, y, p):
        """交叉熵损失"""
        # 避免log(0)
        eps = 1e-15
        p = np.clip(p, eps, 1 - eps)
        return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))
    
    def fit(self, X, y):
        """
        训练模型（梯度下降）
        """
        n_samples, n_features = X.shape
        
        # 初始化参数
        self.coef_ = np.zeros(n_features)
        self.intercept_ = 0
        
        # 梯度下降迭代
        for i in range(self.n_iterations):
            # 计算预测概率
            z = X @ self.coef_ + self.intercept_
            p = self.sigmoid(z)
            
            # 记录损失
            self.loss_history.append(self.cross_entropy_loss(y, p))
            
            # 计算梯度
            gradient_coef = (1 / n_samples) * (X.T @ (p - y))
            gradient_intercept = (1 / n_samples) * np.sum(p - y)
            
            # 更新参数
            self.coef_ -= self.lr * gradient_coef
            self.intercept_ -= self.lr * gradient_intercept
        
        return self
    
    def predict_proba(self, X):
        """预测概率"""
        z = X @ self.coef_ + self.intercept_
        return self.sigmoid(z)
    
    def predict(self, X, threshold=0.5):
        """预测类别"""
        proba = self.predict_proba(X)
        return (proba >= threshold).astype(int)
    
    def score(self, X, y):
        """计算准确率"""
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


# 测试：生成二分类数据
np.random.seed(42)
n_samples = 200

# 两个特征
X = np.random.randn(n_samples, 2)

# 真实决策边界：x1 + x2 > 0 为类别1
y = (X[:, 0] + X[:, 1] > 0).astype(int)

# 训练模型
model = LogisticRegression(learning_rate=0.1, n_iterations=1000)
model.fit(X, y)

print("=== 逻辑回归结果 ===")
print(f"系数: {model.coef_}")
print(f"截距: {model.intercept_:.4f}")
print(f"训练准确率: {model.score(X, y):.3f}")
print(f"最终损失: {model.loss_history[-1]:.4f}")

# 预测示例
print("\n预测示例:")
test_samples = np.array([[1, 1], [-1, -1], [0.5, -0.3]])
proba = model.predict_proba(test_samples)
pred = model.predict(test_samples)
for i, (sample, p, label) in enumerate(zip(test_samples, proba, pred)):
    print(f"样本{i+1}: {sample}, 预测概率={p:.4f}, 预测类别={label}")
```

**输出示例：**
```
=== 逻辑回归结果 ===
系数: [1.23, 1.19]
截距: 0.0123
训练准确率: 0.92
最终损失: 0.21

预测示例:
样本1: [1, 1], 预测概率=0.92, 预测类别=1
样本2: [-1, -1], 预测概率=0.08, 预测类别=0
样本3: [0.5, -0.3], 预测概率=0.55, 预测类别=1
```

### 损失收敛可视化

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(model.loss_history)
plt.xlabel('迭代次数')
plt.ylabel('交叉熵损失')
plt.title('逻辑回归训练过程')
plt.grid(True, alpha=0.3)
plt.savefig('.history/logistic_regression_loss.png')
```

---

## 多分类扩展：Softmax回归

当类别数超过2时，我们需要扩展逻辑回归的思想到多分类场景。

### Softmax函数

设 $K$ 个类别，模型输出 $K$ 个值 $z_1, z_2, \ldots, z_K$。**Softmax函数**将其转换为概率分布：

$$P(y=k) = \frac{e^{z_k}}{\sum_{j=1}^{K} e^{z_j}}$$

每个类别的概率值在(0,1)之间，且所有概率之和为1。

### Softmax回归实现

```python
class SoftmaxRegression:
    """
    Softmax多分类回归实现
    """
    
    def __init__(self, learning_rate=0.1, n_iterations=1000):
        self.lr = learning_rate
        self.n_iterations = n_iterations
        self.W = None  # 权重矩阵 (n_features, n_classes)
        self.loss_history = []
    
    def softmax(self, z):
        """Softmax函数"""
        # 数值稳定性：减去最大值
        z_shifted = z - np.max(z, axis=1, keepdims=True)
        exp_z = np.exp(z_shifted)
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)
    
    def cross_entropy_loss(self, y_true, y_pred):
        """交叉熵损失"""
        eps = 1e-15
        y_pred = np.clip(y_pred, eps, 1 - eps)
        n_samples = y_true.shape[0]
        return -np.sum(y_true * np.log(y_pred)) / n_samples
    
    def fit(self, X, y):
        """
        训练模型
        y: 类别标签 (0, 1, 2, ...)
        """
        n_samples, n_features = X.shape
        n_classes = len(np.unique(y))
        
        # 将标签转换为one-hot编码
        y_onehot = np.zeros((n_samples, n_classes))
        y_onehot[np.arange(n_samples), y] = 1
        
        # 初始化权重
        self.W = np.zeros((n_features, n_classes))
        
        # 梯度下降
        for i in range(self.n_iterations):
            # 计算概率
            z = X @ self.W
            probs = self.softmax(z)
            
            # 记录损失
            self.loss_history.append(self.cross_entropy_loss(y_onehot, probs))
            
            # 计算梯度
            gradient = (1 / n_samples) * (X.T @ (probs - y_onehot))
            
            # 更新权重
            self.W -= self.lr * gradient
        
        return self
    
    def predict_proba(self, X):
        """预测概率分布"""
        z = X @ self.W
        return self.softmax(z)
    
    def predict(self, X):
        """预测类别"""
        probs = self.predict_proba(X)
        return np.argmax(probs, axis=1)
    
    def score(self, X, y):
        """计算准确率"""
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


# 测试：三分类问题
np.random.seed(42)
n_samples = 300

# 生成三类数据点
X = np.random.randn(n_samples, 2)
y = np.zeros(n_samples)
y[X[:, 0] + X[:, 1] > 1] = 1  # 类别1
y[X[:, 0] - X[:, 1] > 1] = 2  # 类别2

model_multi = SoftmaxRegression(learning_rate=0.5, n_iterations=500)
model_multi.fit(X, y)

print(f"训练准确率: {model_multi.score(X, y):.3f}")
print(f"权重矩阵形状: {model_multi.W.shape}")
```

---

## 应用场景示例：客户流失预测

```python
import numpy as np

# 模拟客户数据
np.random.seed(42)
n_customers = 500

# 特征：使用月数、活跃度评分、投诉次数
months = np.random.randint(1, 60, n_customers)
activity_score = np.random.uniform(0, 100, n_customers)
complaints = np.random.randint(0, 5, n_customers)

X = np.column_stack([months, activity_score, complaints])

# 流失逻辑：低活跃度 + 多投诉 = 高流失概率
# 真实流失概率 = sigmoid(-活动评分/50 + 投诉次数*0.5 - 月数/100)
z_true = -activity_score/50 + complaints*0.5 - months/100
churn_prob_true = 1/(1 + np.exp(-z_true))
y = (churn_prob_true > np.random.uniform(0, 1, n_customers)).astype(int)

# 训练模型
model = LogisticRegression(learning_rate=0.01, n_iterations=2000)
model.fit(X, y)

print("=== 客户流失预测模型 ===")
print(f"月数系数: {model.coef_[0]:.4f} (负值表示长期客户更稳定)")
print(f"活跃度系数: {model.coef_[1]:.4f} (正值表示活跃度降低流失风险)")
print(f"投诉系数: {model.coef_[2]:.4f} (正值表示投诉增加流失风险)")
print(f"截距: {model.intercept_:.4f}")
print(f"模型准确率: {model.score(X, y):.3f}")

# 预测高危客户
new_customer = np.array([[12, 30, 3]])  # 12个月，活跃度30，投诉3次
churn_prob = model.predict_proba(new_customer)[0]
print(f"\n新客户流失概率: {churn_prob:.2%}")
```

---

## 小结

本章介绍了逻辑回归的核心原理：

1. **Sigmoid函数**：将线性输出映射到概率，连接回归与分类
2. **交叉熵损失**：从最大似然推导，替代不合理的平方损失
3. **梯度下降优化**：梯度公式简洁，易于实现
4. **Softmax扩展**：将二分类扩展到多分类场景

逻辑回归是分类问题的基石模型。虽然名称中有"回归"二字，但它是真正的分类算法。理解逻辑回归，为后续理解神经网络（其输出层常使用Sigmoid/Softmax）奠定基础。

下一章，我们将讨论如何处理线性模型的"过度学习"问题——正则化与广义线性模型。