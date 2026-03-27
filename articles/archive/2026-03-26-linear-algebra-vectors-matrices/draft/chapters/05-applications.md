# 5. 应用场景：数据表示与特征向量

线性代数不仅是理论工具，更是解决实际问题的关键。本章将展示线性代数在图像处理、文本分析、特征提取和推荐系统中的具体应用，帮助读者理解数学原理如何指导工程实践。

## 5.1 图像数据的矩阵表示

### 灰度图像与矩阵

图像是线性代数最直观的应用场景之一。一张 $m \times n$ 的灰度图像本质上就是一个矩阵：每个矩阵元素表示对应像素的亮度值（0-255）。

```python
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 创建一个简单的灰度图像矩阵
image_matrix = np.array([
    [0, 50, 100, 150, 200, 250],
    [50, 100, 150, 200, 250, 200],
    [100, 150, 200, 250, 200, 150],
    [150, 200, 250, 200, 150, 100],
    [200, 250, 200, 150, 100, 50],
    [250, 200, 150, 100, 50, 0]
], dtype=np.uint8)

print(f"图像矩阵形状: {image_matrix.shape}")  # (6, 6)
print(f"像素值范围: [{image_matrix.min()}, {image_matrix.max()}]")

# 显示图像
plt.imshow(image_matrix, cmap='gray')
plt.colorbar(label='像素值')
plt.title('灰度图像矩阵可视化')
plt.savefig('gray_image.png', dpi=150)
plt.close()
print("图像已保存")
```

### 彩色图像与张量

彩色图像用三个通道（R、G、B）表示，构成一个三维张量：

```python
import numpy as np
from PIL import Image

# 创建一个简单的彩色图像（3×3像素）
# 形状：(高, 宽, 通道)
color_image = np.array([
    [[255, 0, 0], [0, 255, 0], [0, 0, 255]],      # 红, 绿, 蓝
    [[255, 255, 0], [255, 0, 255], [0, 255, 255]], # 黄, 品红, 青
    [[255, 255, 255], [128, 128, 128], [0, 0, 0]]  # 白, 灰, 黑
], dtype=np.uint8)

print(f"彩色图像形状: {color_image.shape}")  # (3, 3, 3)

# 分离各通道
R = color_image[:, :, 0]
G = color_image[:, :, 1]
B = color_image[:, :, 2]

print(f"红色通道:\n{R}")
print(f"绿色通道:\n{G}")
print(f"蓝色通道:\n{B}")
```

### 图像的矩阵操作

矩阵运算可以轻松实现图像的常见操作：

```python
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 加载或创建图像
image = np.random.randint(0, 256, (100, 100), dtype=np.uint8)

# 1. 裁剪：使用切片
cropped = image[25:75, 25:75]  # 中心区域

# 2. 水平翻转：使用切片反转
flipped_h = image[:, ::-1]

# 3. 垂直翻转
flipped_v = image[::-1, :]

# 4. 旋转 90 度
rotated_90 = np.rot90(image)

# 5. 旋转 180 度
rotated_180 = np.rot90(image, 2)

# 6. 转置（对角翻转）
transposed = image.T

print(f"原图形状: {image.shape}")
print(f"裁剪后形状: {cropped.shape}")
```

### 卷积操作的矩阵视角

卷积神经网络（CNN）中的卷积操作，本质上是矩阵的局部运算：

```python
import numpy as np
from scipy.signal import convolve2d

# 简单图像
image = np.array([
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25]
])

# 边缘检测卷积核
edge_kernel = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
])

# 卷积操作
result = convolve2d(image, edge_kernel, mode='valid')
print("卷积结果:\n", result)

# 模糊卷积核
blur_kernel = np.array([
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1]
]) / 9

blurred = convolve2d(image, blur_kernel, mode='valid')
print("\n模糊结果:\n", blurred.round(2))
```

### 图像压缩与奇异值分解

**奇异值分解（SVD）** 可以用于图像压缩：

```python
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# 创建示例图像
image = np.random.rand(200, 200)

# SVD 分解
U, S, Vt = np.linalg.svd(image)

print(f"原始图像形状: {image.shape}")
print(f"奇异值数量: {len(S)}")

# 使用前 k 个奇异值重构图像
def compress_image(U, S, Vt, k):
    """使用前 k 个奇异值重构图像"""
    return U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

# 不同压缩率
ks = [5, 20, 50, 100]
print("\n压缩率分析:")
for k in ks:
    compressed = compress_image(U, S, Vt, k)
    error = np.linalg.norm(image - compressed, 'fro')
    compression_ratio = k * (200 + 200 + 1) / (200 * 200)
    print(f"k={k}: 压缩率={compression_ratio:.2%}, 重构误差={error:.4f}")
```

## 5.2 文本数据的向量化

文本数据需要转换为向量才能被机器学习模型处理。

### 词袋模型（Bag of Words）

词袋模型将文本表示为词汇表中各词出现次数的向量：

```python
from sklearn.feature_extraction.text import CountVectorizer

# 文档集合
documents = [
    "机器学习是人工智能的核心",
    "深度学习是机器学习的子领域",
    "自然语言处理处理文本数据",
    "计算机视觉处理图像数据"
]

# 创建词袋模型
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

print(f"词汇表: {vectorizer.get_feature_names_out()}")
print(f"文档向量矩阵形状: {X.shape}")
print(f"文档向量矩阵:\n{X.toarray()}")

# 每个文档对应一个向量
for i, doc in enumerate(documents):
    print(f"\n文档{i+1}: '{doc}'")
    print(f"向量: {X[i].toarray()}")
```

### TF-IDF

**TF-IDF（词频-逆文档频率）** 考虑了词在文档中的重要性：

```python
from sklearn.feature_extraction.text import TfidfVectorizer

# 使用 TF-IDF
tfidf = TfidfVectorizer()
X_tfidf = tfidf.fit_transform(documents)

print("TF-IDF 矩阵:")
print(X_tfidf.toarray().round(3))

# 查看每个词的 IDF 值
feature_names = tfidf.get_feature_names_out()
idf_values = tfidf.idf_
print("\n各词的 IDF 值:")
for word, idf in sorted(zip(feature_names, idf_values), key=lambda x: x[1], reverse=True):
    print(f"  {word}: {idf:.3f}")
```

### 词向量简介

词向量（Word Embedding）将单词映射为低维稠密向量，语义相近的词在向量空间中距离较近。

```python
import numpy as np

# 模拟词向量（实际应用中使用预训练模型）
word_vectors = {
    "机器学习": np.array([0.8, 0.2, 0.1]),
    "深度学习": np.array([0.9, 0.1, 0.2]),
    "人工智能": np.array([0.7, 0.3, 0.3]),
    "自然语言处理": np.array([0.3, 0.8, 0.4]),
    "计算机视觉": np.array([0.4, 0.3, 0.9]),
    "足球": np.array([0.1, 0.1, 0.1]),
    "篮球": np.array([0.1, 0.2, 0.1])
}

def cosine_similarity(v1, v2):
    """计算余弦相似度"""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 计算词之间的相似度
print("词向量相似度:")
print(f"机器学习 vs 深度学习: {cosine_similarity(word_vectors['机器学习'], word_vectors['深度学习']):.3f}")
print(f"机器学习 vs 自然语言处理: {cosine_similarity(word_vectors['机器学习'], word_vectors['自然语言处理']):.3f}")
print(f"机器学习 vs 足球: {cosine_similarity(word_vectors['机器学习'], word_vectors['足球']):.3f}")

# 词向量运算：类比关系
# "国王" - "男人" + "女人" ≈ "女王"
print("\n词向量类比（简化示例）:")
result = word_vectors['机器学习'] - word_vectors['深度学习'] + word_vectors['自然语言处理']
print(f"机器学习 - 深度学习 + 自然语言处理 ≈ {result.round(2)}")
```

## 5.3 特征向量在机器学习中的意义

### 特征值与特征向量

对于方阵 $\mathbf{A}$，如果存在非零向量 $\mathbf{v}$ 和标量 $\lambda$，使得：

$$\mathbf{A}\mathbf{v} = \lambda\mathbf{v}$$

则 $\mathbf{v}$ 称为 $\mathbf{A}$ 的**特征向量**，$\lambda$ 称为对应的**特征值**。

特征向量的几何意义：在这个方向上，矩阵变换只进行缩放，不改变方向。

```python
import numpy as np

# 定义矩阵
A = np.array([
    [4, 1],
    [2, 3]
])

# 计算特征值和特征向量
eigenvalues, eigenvectors = np.linalg.eig(A)

print("矩阵 A:\n", A)
print("\n特征值:", eigenvalues)
print("特征向量（每列一个）:\n", eigenvectors)

# 验证: A @ v = λ * v
print("\n验证特征向量:")
for i in range(len(eigenvalues)):
    v = eigenvectors[:, i]
    lambda_v = eigenvalues[i]
    Av = A @ v
    lambda_times_v = lambda_v * v
    print(f"特征值 {lambda_v:.2f}: A @ v ≈ λ * v? {np.allclose(Av, lambda_times_v)}")
```

### 主成分分析（PCA）

**PCA** 是特征向量最重要的应用之一。它通过找到数据方差最大的方向来实现降维。

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 生成二维数据（有相关性）
np.random.seed(42)
n_samples = 200
mean = [0, 0]
cov = [[3, 2], [2, 2]]  # 协方差矩阵
data = np.random.multivariate_normal(mean, cov, n_samples)

print(f"原始数据形状: {data.shape}")

# 方法一：使用 sklearn
pca = PCA(n_components=2)
pca.fit(data)

print(f"\n主成分方向（特征向量）:\n{pca.components_}")
print(f"解释方差比例: {pca.explained_variance_ratio_}")
print(f"特征值: {pca.explained_variance_}")

# 方法二：手动实现 PCA
# 1. 中心化
data_centered = data - data.mean(axis=0)

# 2. 计算协方差矩阵
cov_matrix = np.cov(data_centered.T)

# 3. 特征分解
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

# 4. 排序（按特征值降序）
idx = eigenvalues.argsort()[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

print(f"\n手动计算结果:")
print(f"特征值: {eigenvalues}")
print(f"特征向量:\n{eigenvectors}")

# 降维到一维
pca_1d = PCA(n_components=1)
data_1d = pca_1d.fit_transform(data)
print(f"\n降维后形状: {data_1d.shape}")

# 可视化
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.scatter(data[:, 0], data[:, 1], alpha=0.5)
origin = data.mean(axis=0)
for i, (length, vector) in enumerate(zip(pca.explained_variance_, pca.components_)):
    v = vector * 2 * np.sqrt(length)
    plt.arrow(origin[0], origin[1], v[0], v[1], head_width=0.3, head_length=0.2,
              fc=f'C{i+1}', ec=f'C{i+1}', linewidth=2, label=f'PC{i+1}')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('原始数据与主成分方向')
plt.grid(True)
plt.axis('equal')

plt.subplot(1, 2, 2)
plt.scatter(data_1d, np.zeros_like(data_1d), alpha=0.5)
plt.xlabel('主成分')
plt.title('降维后数据（一维）')
plt.grid(True)

plt.tight_layout()
plt.savefig('pca_demo.png', dpi=150)
plt.close()
print("PCA 演示图已保存")
```

### 特征脸简介

特征脸（Eigenface）是人脸识别的经典方法，将人脸图像表示为"特征脸"的线性组合：

```python
import numpy as np
from sklearn.datasets import fetch_olivetti_faces
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 加载人脸数据集（如果网络不可用，可用随机数据模拟）
try:
    faces = fetch_olivetti_faces(shuffle=True, random_state=42)
    X = faces.data  # (400, 4096) - 400张64x64的人脸图像
except:
    # 模拟数据
    X = np.random.rand(100, 4096)

print(f"人脸数据形状: {X.shape}")  # (样本数, 像素数)

# PCA 降维
n_components = 50
pca = PCA(n_components=n_components, whiten=True)
X_pca = pca.fit_transform(X)

print(f"降维后形状: {X_pca.shape}")
print(f"累计解释方差: {sum(pca.explained_variance_ratio_):.2%}")

# 可视化前几个"特征脸"
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for i, ax in enumerate(axes.flat):
    if i < n_components:
        ax.imshow(pca.components_[i].reshape(64, 64), cmap='gray')
        ax.set_title(f'特征脸 {i+1}')
    ax.axis('off')
plt.suptitle('特征脸（Eigenfaces）')
plt.tight_layout()
plt.savefig('eigenfaces.png', dpi=150)
plt.close()
print("特征脸图已保存")
```

## 5.4 推荐系统中的矩阵方法

### 协同过滤

协同过滤是推荐系统的经典方法，基于用户行为相似性进行推荐。

```python
import numpy as np

# 用户-物品评分矩阵
# 行：用户，列：物品，值：评分（0表示未评分）
ratings = np.array([
    [5, 3, 0, 1, 0, 0],  # 用户1
    [4, 0, 0, 1, 0, 2],  # 用户2
    [1, 1, 0, 5, 4, 0],  # 用户3
    [0, 0, 0, 4, 0, 5],  # 用户4
    [0, 1, 5, 4, 0, 0],  # 用户5
])

print("用户-物品评分矩阵:")
print(ratings)
print(f"矩阵形状: {ratings.shape}")

# 用户相似度（余弦相似度）
def cosine_similarity_matrix(matrix):
    """计算矩阵行之间的余弦相似度"""
    # 归一化
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1  # 避免除零
    normalized = matrix / norms
    # 计算相似度
    return normalized @ normalized.T

user_sim = cosine_similarity_matrix(ratings)
print("\n用户相似度矩阵:")
print(user_sim.round(3))
```

### 矩阵分解技术

矩阵分解将评分矩阵分解为用户矩阵和物品矩阵的乘积：

```python
import numpy as np
from scipy.sparse.linalg import svds

# 使用 SVD 进行矩阵分解
# 首先填充缺失值（用均值）
ratings_filled = ratings.copy()
ratings_filled[ratings_filled == 0] = ratings[ratings > 0].mean()

# SVD 分解
k = 2  # 隐因子数量
U, sigma, Vt = svds(ratings_filled, k=k)

print(f"U (用户矩阵) 形状: {U.shape}")
print(f"sigma (奇异值) 形状: {sigma.shape}")
print(f"Vt (物品矩阵) 形状: {Vt.shape}")

# 重构评分矩阵
predicted_ratings = U @ np.diag(sigma) @ Vt

print("\n预测评分矩阵:")
print(predicted_ratings.round(2))

# 推荐给用户1的物品
user1_predicted = predicted_ratings[0]
user1_actual = ratings[0]
# 找出用户1未评分但预测评分高的物品
recommend_items = np.where(user1_actual == 0)[0]
recommended = sorted(recommend_items, key=lambda x: user1_predicted[x], reverse=True)
print(f"\n推荐给用户1的物品: {recommended}")
```

### 低秩近似

低秩近似用于数据压缩和降噪：

```python
import numpy as np

# 创建一个低秩矩阵（加噪声）
np.random.seed(42)
U_true = np.random.randn(10, 3)
V_true = np.random.randn(3, 5)
matrix = U_true @ V_true + 0.1 * np.random.randn(10, 5)

print(f"原始矩阵形状: {matrix.shape}")

# SVD 分解
U, S, Vt = np.linalg.svd(matrix, full_matrices=False)

print(f"\n奇异值: {S.round(3)}")

# 低秩近似
def low_rank_approximation(U, S, Vt, k):
    """保留前 k 个奇异值的低秩近似"""
    return U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

# 不同秩的近似
print("\n低秩近似误差:")
for k in [1, 2, 3, 5]:
    approx = low_rank_approximation(U, S, Vt, k)
    error = np.linalg.norm(matrix - approx, 'fro')
    print(f"秩 {k}: 重构误差 = {error:.4f}")
```

---

## 本章小结

本章展示了线性代数在机器学习中的实际应用：

1. **图像处理**：图像即矩阵，矩阵运算实现图像操作，SVD 实现压缩
2. **文本分析**：文本向量化（词袋、TF-IDF、词向量），余弦相似度计算
3. **特征提取**：特征值分解、PCA 降维、特征脸
4. **推荐系统**：协同过滤、矩阵分解、低秩近似

这些应用展示了线性代数不仅是理论工具，更是解决实际问题的基础。

下一章将回顾全文要点，并提供思考题和扩展阅读。