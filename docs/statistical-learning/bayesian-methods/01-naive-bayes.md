# 朴素贝叶斯——最简单的概率分类器

## 引言：贝叶斯思维在机器学习中的实践

在[概率统计系列](../../maths/probability/introduction.md)中，我们学习了贝叶斯定理：

$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

这个简洁的公式揭示了一个深刻的思想：**用新证据更新我们对世界的认知**。当我们观察到证据 $B$，我们对事件 $A$ 发生的信念从先验概率 $P(A)$ 更新为后验概率 $P(A|B)$。

机器学习的本质正是"从数据中学习规律"。当我们面对一个分类问题时，贝叶斯思维告诉我们：**分类就是计算"给定特征，属于各类别的概率"，选择概率最大的类别**。

$$P(y=c|X) = \frac{P(X|y=c) \cdot P(y=c)}{P(X)}$$

然而，直接计算 $P(X|y=c)$ 在高维特征空间中几乎不可能——需要估计所有特征的联合概率分布。**朴素贝叶斯（Naive Bayes）**用一个"朴素"的假设破解了这个困境：**假设所有特征相互独立**。

这个假设在实际中几乎从不成立，但朴素贝叶斯却经常出人意料地有效。为什么？这正是本章要探讨的核心问题。

---

## 条件独立性假设：从朴素到实用

### 贝叶斯分类器原理

给定特征向量 $X = (x_1, x_2, \ldots, x_d)$，我们要预测类别 $y$。根据贝叶斯定理：

$$P(y|X) = \frac{P(X|y) \cdot P(y)}{P(X)}$$

对于分类任务，我们只需要比较不同类别的后验概率大小，分母 $P(X)$ 对所有类别相同，可以忽略。分类决策规则：

$$\hat{y} = \arg\max_c P(y=c) \cdot P(X|y=c)$$

### 朴素假设的引入

计算 $P(X|y=c) = P(x_1, x_2, \ldots, x_d | y=c)$ 需要知道 $d$ 个特征的联合分布。如果每个特征有 $v$ 个可能取值，需要估计 $v^d$ 个概率值——特征维度稍高就不可行。

**朴素假设**：假设在给定类别 $y$ 的条件下，各特征相互独立：

$$P(X|y=c) = \prod_{j=1}^{d} P(x_j | y=c)$$

这个假设将联合概率估计从 $v^d$ 降到 $d \times v$，使得高维问题的概率估计成为可能。

### 分类公式

结合朴素假设，朴素贝叶斯分类器：

$$\hat{y} = \arg\max_c P(y=c) \prod_{j=1}^{d} P(x_j | y=c)$$

实际计算中，多个小概率相乘容易导致数值下溢，通常取对数：

$$\hat{y} = \arg\max_c \left[ \log P(y=c) + \sum_{j=1}^{d} \log P(x_j | y=c) \right]$$

### 为什么"朴素"假设有效？

朴素假设在实际中几乎从不成立——特征之间往往存在相关性。那么为什么朴素贝叶斯仍然有效？

1. **分类只关心相对大小**：即使概率估计不准确，只要各类别的相对排序正确，分类结果就是正确的
2. **决策边界简化**：朴素贝叶斯是线性分类器的一种，决策边界由对数概率比决定
3. **偏差-方差权衡**：朴素假设引入偏差，但大大减少方差，在小样本场景反而有优势

---

## NumPy实现：离散型朴素贝叶斯

离散型朴素贝叶斯适用于特征为离散值（如词频、类别）的场景。最典型的应用是文本分类。

```python
import numpy as np
from collections import Counter

class MultinomialNaiveBayes:
    """
    多项式朴素贝叶斯实现
    适用于离散特征（如文本词频）
    """
    
    def __init__(self, alpha=1.0):
        """
        Parameters:
        alpha : float, 拉普拉斯平滑参数
        """
        self.alpha = alpha  # 拉普拉斯平滑
        self.class_prior_ = None  # P(y)
        self.feature_prob_ = None  # P(x|y)
        self.classes_ = None
    
    def fit(self, X, y):
        """
        训练模型
        
        Parameters:
        X : ndarray, shape (n_samples, n_features)
            特征矩阵（词频/计数）
        y : ndarray, shape (n_samples,)
            类别标签
        """
        n_samples, n_features = X.shape
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        
        # 计算先验概率 P(y)
        class_counts = np.array([np.sum(y == c) for c in self.classes_])
        self.class_prior_ = class_counts / n_samples
        
        # 计算条件概率 P(x|y)
        # 对于每个类别，计算每个特征在该类别文档中的总计数
        self.feature_prob_ = np.zeros((n_classes, n_features))
        
        for i, c in enumerate(self.classes_):
            # 获取类别c的所有样本
            X_c = X[y == c]
            # 该类别每个特征的总计数 + 平滑
            feature_counts = X_c.sum(axis=0) + self.alpha
            # 归一化得到条件概率
            total_count = feature_counts.sum()
            self.feature_prob_[i] = feature_counts / total_count
        
        return self
    
    def predict_log_proba(self, X):
        """
        计算对数概率
        """
        # log P(y) + sum(log P(x|y))
        log_prior = np.log(self.class_prior_)
        log_likelihood = X @ np.log(self.feature_prob_.T)  # (n_samples, n_classes)
        return log_prior + log_likelihood
    
    def predict(self, X):
        """
        预测类别
        """
        log_proba = self.predict_log_proba(X)
        return self.classes_[np.argmax(log_proba, axis=1)]
    
    def score(self, X, y):
        """计算准确率"""
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


# 测试：简单的文本分类
np.random.seed(42)

# 模拟词频数据（5个词，4个文档）
# 特征：["好", "坏", "喜欢", "讨厌", "一般"]
X_train = np.array([
    [3, 0, 2, 0, 1],  # 文档1：好词多 → 正面
    [2, 1, 1, 0, 1],  # 文档2：偏正面
    [0, 3, 0, 2, 1],  # 文档3：坏词多 → 负面
    [1, 2, 0, 1, 2],  # 文档4：偏负面
])
y_train = np.array(['正面', '正面', '负面', '负面'])

# 训练模型
model = MultinomialNaiveBayes(alpha=1.0)
model.fit(X_train, y_train)

print("=== 朴素贝叶斯文本分类 ===")
print(f"类别: {model.classes_}")
print(f"先验概率: {dict(zip(model.classes_, model.class_prior_))}")

# 预测新文档
X_test = np.array([
    [2, 0, 1, 0, 0],  # 明显正面
    [0, 2, 0, 2, 0],  # 明显负面
    [1, 1, 1, 1, 1],  # 中性
])
y_pred = model.predict(X_test)
print(f"\n测试文档预测: {y_pred}")

# 输出概率
log_proba = model.predict_log_proba(X_test)
print(f"对数概率:\n{log_proba}")
```

**输出示例：**
```
=== 朴素贝叶斯文本分类 ===
类别: ['正面' '负面']
先验概率: {'正面': 0.5, '负面': 0.5}

测试文档预测: ['正面' '负面' '负面']
对数概率:
[[ -2.3  -4.5]
 [ -6.7  -3.1]
 [ -5.2  -4.8]]
```

### 拉普拉斯平滑

朴素贝叶斯有一个重要问题：**如果某个特征在训练集中从未出现过，则 $P(x|y)=0$，导致整个概率乘积为0**。

解决方案是**拉普拉斯平滑（Laplace Smoothing）**：

$$P(x_j | y=c) = \frac{N_{jc} + \alpha}{N_c + \alpha \cdot V}$$

其中：
- $N_{jc}$：类别 $c$ 中特征 $j$ 的出现次数
- $N_c$：类别 $c$ 的样本总数
- $\alpha$：平滑参数（通常为1）
- $V$：特征总数

这确保了所有概率值都大于0。

---

## NumPy实现：Gaussian朴素贝叶斯

当特征是连续值时，假设特征服从高斯分布：

$$P(x_j | y=c) = \frac{1}{\sqrt{2\pi\sigma_{jc}^2}} \exp\left(-\frac{(x_j - \mu_{jc})^2}{2\sigma_{jc}^2}\right)$$

```python
class GaussianNaiveBayes:
    """
    高斯朴素贝叶斯实现
    适用于连续特征
    """
    
    def __init__(self):
        self.classes_ = None
        self.class_prior_ = None
        self.mu_ = None  # 每个类别每个特征的均值
        self.sigma_ = None  # 每个类别每个特征的标准差
    
    def fit(self, X, y):
        """训练模型"""
        n_samples, n_features = X.shape
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        
        # 先验概率
        class_counts = np.array([np.sum(y == c) for c in self.classes_])
        self.class_prior_ = class_counts / n_samples
        
        # 计算每个类别的均值和标准差
        self.mu_ = np.zeros((n_classes, n_features))
        self.sigma_ = np.zeros((n_classes, n_features))
        
        for i, c in enumerate(self.classes_):
            X_c = X[y == c]
            self.mu_[i] = X_c.mean(axis=0)
            self.sigma_[i] = X_c.std(axis=0) + 1e-9  # 防止除零
        
        return self
    
    def _gaussian_pdf(self, X, mu, sigma):
        """计算高斯概率密度"""
        return np.exp(-0.5 * ((X - mu) / sigma)**2) / (sigma * np.sqrt(2 * np.pi))
    
    def predict_log_proba(self, X):
        """计算对数概率"""
        n_samples = X.shape[0]
        n_classes = len(self.classes_)
        log_proba = np.zeros((n_samples, n_classes))
        
        for i in range(n_classes):
            # log P(y) + sum(log P(x|y))
            log_prior = np.log(self.class_prior_[i])
            # 对数概率密度
            log_likelihood = np.sum(
                -0.5 * np.log(2 * np.pi) 
                - np.log(self.sigma_[i]) 
                - 0.5 * ((X - self.mu_[i]) / self.sigma_[i])**2,
                axis=1
            )
            log_proba[:, i] = log_prior + log_likelihood
        
        return log_proba
    
    def predict(self, X):
        """预测类别"""
        log_proba = self.predict_log_proba(X)
        return self.classes_[np.argmax(log_proba, axis=1)]
    
    def score(self, X, y):
        """计算准确率"""
        y_pred = self.predict(X)
        return np.mean(y_pred == y)


# 测试：鸢尾花分类
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data
y = iris.target

# 划分训练测试集
n_samples = len(X)
indices = np.random.permutation(n_samples)
split = int(0.8 * n_samples)
X_train, X_test = X[indices[:split]], X[indices[split:]]
y_train, y_test = y[indices[:split]], y[indices[split:]]

# 训练模型
model = GaussianNaiveBayes()
model.fit(X_train, y_train)

print("=== 高斯朴素贝叶斯：鸢尾花分类 ===")
print(f"训练准确率: {model.score(X_train, y_train):.3f}")
print(f"测试准确率: {model.score(X_test, y_test):.3f}")

# 各类别的特征均值
print("\n各类别的特征均值:")
for i, c in enumerate(iris.target_names):
    print(f"  {c}: {model.mu_[i]}")
```

**输出示例：**
```
=== 高斯朴素贝叶斯：鸢尾花分类 ===
训练准确率: 0.958
测试准确率: 0.933

各类别的特征均值:
  setosa: [5.0 3.4 1.5 0.2]
  versicolor: [5.9 2.8 4.3 1.3]
  virginica: [6.6 3.0 5.6 2.0]
```

---

## 应用场景：文本分类实战

```python
import numpy as np

# 模拟邮件分类数据
emails = [
    ("买一送一 限时优惠 点击领取", "垃圾邮件"),
    ("明天开会 请准时参加", "正常邮件"),
    ("免费抽奖 中奖概率100%", "垃圾邮件"),
    ("项目进度报告 请查收", "正常邮件"),
    ("贷款审批通过 即刻放款", "垃圾邮件"),
    ("周末聚餐 时间地点确认", "正常邮件"),
    ("点击链接 领取红包", "垃圾邮件"),
    ("客户需求讨论 会议纪要", "正常邮件"),
]

# 简单的词袋模型
def tokenize(text):
    """分词（简单空格分割）"""
    return text.lower().split()

# 构建词汇表
vocab = set()
for text, _ in emails:
    vocab.update(tokenize(text))
vocab = sorted(vocab)
word_to_idx = {w: i for i, w in enumerate(vocab)}

print(f"词汇表大小: {len(vocab)}")
print(f"词汇表: {vocab[:10]}...")

# 转换为词频矩阵
def text_to_vector(text):
    vec = np.zeros(len(vocab))
    for word in tokenize(text):
        if word in word_to_idx:
            vec[word_to_idx[word]] += 1
    return vec

X = np.array([text_to_vector(text) for text, _ in emails])
y = np.array([label for _, label in emails])

# 训练朴素贝叶斯
model = MultinomialNaiveBayes(alpha=1.0)
model.fit(X, y)

print(f"\n=== 邮件分类模型 ===")
print(f"训练准确率: {model.score(X, y):.3f}")

# 测试新邮件
test_emails = [
    "点击领取 免费红包",
    "会议时间 明天下午",
    "贷款审批 通过",
]

test_X = np.array([text_to_vector(text) for text in test_emails])
predictions = model.predict(test_X)

print("\n新邮件预测:")
for email, pred in zip(test_emails, predictions):
    print(f"  '{email}' → {pred}")
```

---

## 小结

本章介绍了朴素贝叶斯分类器：

1. **贝叶斯思维**：分类本质是计算后验概率，选择概率最大的类别
2. **朴素假设**：特征条件独立，将联合概率估计简化为边际概率的乘积
3. **离散型**：多项式朴素贝叶斯适用于文本等离散特征
4. **连续型**：高斯朴素贝叶斯适用于连续特征
5. **拉普拉斯平滑**：解决零概率问题，防止乘积为零

朴素贝叶斯虽然假设"朴素"，但因其简单高效、对小样本友好，在文本分类、垃圾邮件过滤等场景仍有广泛应用。下一章，我们将看到如何放松独立假设——贝叶斯网络。