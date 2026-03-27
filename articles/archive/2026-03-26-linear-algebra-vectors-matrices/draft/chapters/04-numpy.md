# 4. Python 实践：NumPy 数组操作

NumPy（Numerical Python）是 Python 科学计算的基石，提供了高效的多维数组对象和丰富的数学函数。本章将深入讲解 NumPy 的核心操作，帮助读者掌握向量化编程的技巧。

## 4.1 NumPy 数组创建与基本属性

### 从列表创建数组

NumPy 的核心是 `ndarray`（N-dimensional array）对象，即多维数组。最简单的创建方式是从 Python 列表转换：

```python
import numpy as np

# 一维数组
arr1d = np.array([1, 2, 3, 4, 5])
print(f"一维数组: {arr1d}")
print(f"类型: {type(arr1d)}")

# 二维数组（矩阵）
arr2d = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
print(f"二维数组:\n{arr2d}")

# 三维数组
arr3d = np.array([
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]]
])
print(f"三维数组形状: {arr3d.shape}")  # (2, 2, 2)
```

### 特殊数组创建

NumPy 提供了多种创建特殊数组的函数：

```python
import numpy as np

# 全零数组
zeros = np.zeros((3, 4))  # 3×4 全零矩阵
print(f"zeros:\n{zeros}")

# 全一数组
ones = np.ones((2, 3))  # 2×3 全一矩阵
print(f"ones:\n{ones}")

# 单位矩阵
eye = np.eye(4)  # 4×4 单位矩阵
print(f"单位矩阵:\n{eye}")

# 空矩阵（未初始化，内容随机）
empty = np.empty((2, 2))
print(f"空矩阵:\n{empty}")

# 等差序列
arange_arr = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
print(f"arange: {arange_arr}")

# 等间隔序列
linspace_arr = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]
print(f"linspace: {linspace_arr}")

# 对角矩阵
diag = np.diag([1, 2, 3])  # 对角元素为 1, 2, 3
print(f"对角矩阵:\n{diag}")
```

### 随机数组生成

机器学习中经常需要生成随机数据：

```python
import numpy as np

# 设置随机种子（保证可重复性）
np.random.seed(42)

# [0, 1) 均匀分布
rand_arr = np.random.rand(2, 3)  # 2×3 随机矩阵
print(f"均匀分布:\n{rand_arr}")

# 标准正态分布
randn_arr = np.random.randn(2, 3)  # 均值0，方差1
print(f"正态分布:\n{randn_arr}")

# 指定范围整数
randint_arr = np.random.randint(0, 10, (2, 3))  # [0, 10) 范围整数
print(f"随机整数:\n{randint_arr}")

# 正态分布（指定参数）
normal_arr = np.random.normal(loc=0, scale=1, size=(2, 3))
print(f"指定正态分布:\n{normal_arr}")

# 随机打乱
arr = np.array([1, 2, 3, 4, 5])
np.random.shuffle(arr)
print(f"打乱后: {arr}")

# 随机选择
choices = np.random.choice([1, 2, 3, 4, 5], size=3, replace=False)
print(f"随机选择: {choices}")
```

### 数组的基本属性

```python
arr = np.array([
    [[1, 2, 3], [4, 5, 6]],
    [[7, 8, 9], [10, 11, 12]]
])

print(f"数组:\n{arr}")
print(f"形状 (shape): {arr.shape}")    # (2, 2, 3)
print(f"维度 (ndim): {arr.ndim}")      # 3
print(f"数据类型 (dtype): {arr.dtype}") # int64
print(f"元素总数 (size): {arr.size}")   # 12
print(f"每个元素字节大小: {arr.itemsize}")  # 8
print(f"总字节大小: {arr.nbytes}")      # 96
```

### 数组的数据类型转换

NumPy 支持多种数据类型，可以显式指定或转换：

```python
import numpy as np

# 创建时指定类型
arr_float = np.array([1, 2, 3], dtype=np.float32)
print(f"浮点数组: {arr_float}, dtype: {arr_float.dtype}")

# 类型转换
arr_int = arr_float.astype(np.int32)
print(f"整数数组: {arr_int}, dtype: {arr_int.dtype}")

# 常见数据类型
print("\n常见数据类型:")
print(f"bool: {np.array([True, False]).dtype}")
print(f"int8: {np.array([1], dtype=np.int8).dtype}")
print(f"int32: {np.array([1], dtype=np.int32).dtype}")
print(f"int64: {np.array([1], dtype=np.int64).dtype}")
print(f"float32: {np.array([1.0], dtype=np.float32).dtype}")
print(f"float64: {np.array([1.0], dtype=np.float64).dtype}")
```

## 4.2 索引与切片

### 一维数组索引

一维数组的索引与 Python 列表相同：

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

print(f"数组: {arr}")
print(f"arr[0]: {arr[0]}")    # 第一个元素
print(f"arr[-1]: {arr[-1]}")  # 最后一个元素
print(f"arr[1:4]: {arr[1:4]}")  # 切片 [20, 30, 40]
print(f"arr[::2]: {arr[::2]}")  # 步长为2 [10, 30, 50]
print(f"arr[::-1]: {arr[::-1]}")  # 反转
```

### 多维数组索引

多维数组使用逗号分隔各维度的索引：

```python
import numpy as np

arr = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
])

print(f"数组形状: {arr.shape}")  # (3, 4)
print(f"arr[0, 1]: {arr[0, 1]}")    # 第0行第1列: 2
print(f"arr[1]: {arr[1]}")          # 第1行: [5, 6, 7, 8]
print(f"arr[:, 0]: {arr[:, 0]}")    # 第0列: [1, 5, 9]
print(f"arr[0:2, 1:3]:\n{arr[0:2, 1:3]}")  # 子矩阵
# [[2 3]
#  [6 7]]
```

### 切片操作

切片返回的是**视图（View）**而非副本，修改视图会影响原数组：

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 获取子矩阵（视图）
sub = arr[:2, 1:]
print(f"子矩阵:\n{sub}")

# 修改视图会影响原数组
sub[0, 0] = 100
print(f"修改后的原数组:\n{arr}")
# [[  1 100   3]
#  [  4   5   6]
#  [  7   8   9]]

# 如果需要副本，使用 copy()
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
sub_copy = arr[:2, 1:].copy()
sub_copy[0, 0] = 100
print(f"使用 copy() 后原数组不变:\n{arr}")
```

### 布尔索引

布尔索引用于根据条件筛选元素：

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# 创建布尔掩码
mask = arr > 5
print(f"布尔掩码: {mask}")

# 使用布尔索引
print(f"大于5的元素: {arr[mask]}")

# 直接在索引中使用条件
print(f"偶数: {arr[arr % 2 == 0]}")

# 复合条件
print(f"大于3且小于8: {arr[(arr > 3) & (arr < 8)]}")

# 多维数组的布尔索引
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"大于5的元素: {matrix[matrix > 5]}")
```

### 花式索引（Fancy Indexing）

花式索引使用整数数组作为索引：

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])

# 使用索引数组
indices = [0, 2, 4]
print(f"索引 {indices} 的元素: {arr[indices]}")

# 使用负索引
print(f"arr[[0, -1]]: {arr[[0, -1]]}")  # 第一个和最后一个

# 多维花式索引
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# 选择特定行
print(f"第0行和第2行:\n{matrix[[0, 2]]}")

# 选择特定位置的元素
rows = [0, 1, 2]
cols = [2, 1, 0]
print(f"对角线元素 (反): {matrix[rows, cols]}")  # [3, 5, 7]

# 使用 np.ix_ 创建索引器
print(f"选择特定行列:\n{matrix[np.ix_([0, 2], [0, 2])]}")
# [[1 3]
#  [7 9]]
```

## 4.3 广播机制详解

### 广播的概念

**广播（Broadcasting）** 是 NumPy 处理不同形状数组运算的强大机制。当两个数组形状不同时，NumPy 会自动扩展较小的数组，使其能够与较大的数组进行运算。

```python
import numpy as np

# 标量与数组
a = np.array([1, 2, 3])
b = 2
result = a + b
print(f"{a} + {b} = {result}")  # [3, 4, 5]

# 不同形状数组
A = np.array([[1, 2, 3], [4, 5, 6]])  # (2, 3)
v = np.array([10, 20, 30])            # (3,)
result = A + v
print(f"广播结果:\n{result}")
# [[11 22 33]
#  [14 25 36]]
```

### 广播的规则

广播遵循三条规则：

1. **维度对齐**：如果两个数组的维度不同，在较小数组的形状前面补 1
2. **兼容检查**：如果两个数组在某个维度上大小相同，或其中一个为 1，则它们在该维度上兼容
3. **扩展**：在所有维度都兼容时，大小为 1 的维度会被扩展

```python
import numpy as np

def explain_broadcast(shape1, shape2):
    """解释广播过程"""
    arr1 = np.zeros(shape1)
    arr2 = np.ones(shape2)

    try:
        result = arr1 + arr2
        print(f"形状 {shape1} + 形状 {shape2} -> 形状 {result.shape}")
        print(f"广播后形状: {np.broadcast_shapes(shape1, shape2)}")
        return True
    except ValueError as e:
        print(f"形状 {shape1} + 形状 {shape2} -> 错误: {e}")
        return False

# 示例
explain_broadcast((3, 4), (4,))       # 可广播
explain_broadcast((3, 4), (3, 1))     # 可广播
explain_broadcast((3, 4), (1, 4))     # 可广播
explain_broadcast((3, 4), (3,))       # 可广播
explain_broadcast((3, 4), (2, 4))     # 不可广播
```

### 广播的常见场景

**1. 数据标准化**

```python
import numpy as np

# 模拟数据集：100个样本，50个特征
data = np.random.randn(100, 50)

# 计算每个特征的均值和标准差
means = data.mean(axis=0)  # (50,)
stds = data.std(axis=0)    # (50,)

# 标准化：广播使 (100, 50) 与 (50,) 运算
normalized = (data - means) / stds

print(f"原始数据形状: {data.shape}")
print(f"均值形状: {means.shape}")
print(f"标准化后形状: {normalized.shape}")
print(f"标准化后均值: {normalized.mean(axis=0)[:5]}")  # 接近0
```

**2. 外积**

```python
import numpy as np

a = np.array([1, 2, 3])    # (3,)
b = np.array([10, 20])     # (2,)

# 方法一：广播
outer = a.reshape(3, 1) * b.reshape(1, 2)
print(f"外积 (广播):\n{outer}")

# 方法二：np.outer
outer2 = np.outer(a, b)
print(f"外积 (np.outer):\n{outer2}")
```

**3. 距离矩阵**

```python
import numpy as np

# 两点集之间的距离
points1 = np.random.rand(5, 2)  # 5个点，2维
points2 = np.random.rand(3, 2)  # 3个点，2维

# 使用广播计算距离矩阵
# (5, 1, 2) - (1, 3, 2) -> (5, 3, 2)
diff = points1[:, np.newaxis, :] - points2[np.newaxis, :, :]
distances = np.sqrt((diff ** 2).sum(axis=2))  # (5, 3)

print(f"点集1形状: {points1.shape}")
print(f"点集2形状: {points2.shape}")
print(f"距离矩阵形状: {distances.shape}")
```

### 避免隐式广播的陷阱

```python
import numpy as np

# 陷阱示例：意外的广播
A = np.array([[1, 2], [3, 4], [5, 6]])  # (3, 2)
v = np.array([10, 20, 30])               # (3,)

try:
    result = A + v
except ValueError as e:
    print(f"错误: {e}")
    # 解决方法：明确指定维度
    result = A + v[:, np.newaxis]  # (3, 2) + (3, 1) -> (3, 2)
    print(f"正确结果:\n{result}")
```

## 4.4 向量化运算 vs 循环

### 向量化的概念

**向量化（Vectorization）** 是指用数组运算替代显式循环。NumPy 的底层是 C 语言实现，利用了 SIMD（单指令多数据）指令，可以带来数量级的性能提升。

### 性能对比实验

```python
import numpy as np
import time

# 创建大数组
n = 10_000_000
a = np.random.rand(n)
b = np.random.rand(n)

# 方法一：Python 循环
start = time.time()
result_loop = np.zeros(n)
for i in range(n):
    result_loop[i] = a[i] + b[i]
loop_time = time.time() - start
print(f"循环耗时: {loop_time:.4f} 秒")

# 方法二：NumPy 向量化
start = time.time()
result_vec = a + b
vec_time = time.time() - start
print(f"向量化耗时: {vec_time:.4f} 秒")
print(f"性能提升: {loop_time/vec_time:.1f} 倍")

# 验证结果一致
print(f"结果一致: {np.allclose(result_loop, result_vec)}")
```

### 常用向量化函数

```python
import numpy as np

arr = np.random.rand(1000, 1000)

# 数学函数（逐元素）
np.exp(arr)      # 指数
np.log(arr)      # 对数
np.sqrt(arr)     # 平方根
np.abs(arr)      # 绝对值
np.power(arr, 2) # 幂次

# 三角函数
np.sin(arr)
np.cos(arr)
np.tan(arr)

# 聚合函数
np.sum(arr)      # 总和
np.mean(arr)     # 均值
np.std(arr)      # 标准差
np.var(arr)      # 方差
np.max(arr)      # 最大值
np.min(arr)      # 最小值
np.argmax(arr)   # 最大值索引
np.argmin(arr)   # 最小值索引

# 沿指定轴聚合
np.sum(arr, axis=0)   # 沿列求和
np.mean(arr, axis=1)  # 沿行求均值

# 统计函数
np.median(arr)
np.percentile(arr, 50)
np.unique(arr)
np.bincount(arr.astype(int))
```

### 向量化技巧

**1. 避免 Python 循环**

```python
import numpy as np

# 不好的做法
def sigmoid_loop(arr):
    result = np.zeros_like(arr)
    for i in range(len(arr)):
        result[i] = 1 / (1 + np.exp(-arr[i]))
    return result

# 好的做法
def sigmoid_vectorized(arr):
    return 1 / (1 + np.exp(-arr))

arr = np.random.randn(1000000)
%timeit sigmoid_loop(arr)       # 慢
%timeit sigmoid_vectorized(arr) # 快很多
```

**2. 使用 np.where 替代条件循环**

```python
import numpy as np

arr = np.random.randn(1000)

# 不好的做法
result = np.zeros_like(arr)
for i in range(len(arr)):
    if arr[i] > 0:
        result[i] = arr[i]
    else:
        result[i] = 0

# 好的做法
result = np.where(arr > 0, arr, 0)
# 或者
result = np.maximum(arr, 0)  # ReLU
```

**3. 使用 np.einsum 进行复杂运算**

```python
import numpy as np

# 矩阵乘法
A = np.random.rand(100, 50)
B = np.random.rand(50, 80)

# 常规方法
C1 = A @ B

# einsum 方法（更灵活）
C2 = np.einsum('ij,jk->ik', A, B)

print(f"结果一致: {np.allclose(C1, C2)}")

# 更复杂的例子：批量矩阵乘法
batch_A = np.random.rand(10, 100, 50)
batch_B = np.random.rand(10, 50, 80)
batch_C = np.einsum('bij,bjk->bik', batch_A, batch_B)
print(f"批量矩阵乘法形状: {batch_C.shape}")
```

## 4.5 矩阵运算实践

### 矩阵乘法实现

```python
import numpy as np

# 矩阵乘法的多种实现
A = np.random.rand(100, 50)
B = np.random.rand(50, 80)

# 方法一：@ 运算符（推荐）
C1 = A @ B

# 方法二：np.matmul
C2 = np.matmul(A, B)

# 方法三：np.dot
C3 = np.dot(A, B)

# 方法四：np.einsum
C4 = np.einsum('ij,jk->ik', A, B)

print(f"所有方法结果一致: {np.allclose(C1, C2) and np.allclose(C2, C3) and np.allclose(C3, C4)}")
```

### 矩阵分解

NumPy 提供了常用的矩阵分解方法：

```python
import numpy as np

# 创建对称正定矩阵
A = np.random.rand(5, 5)
A = A @ A.T + np.eye(5) * 0.1  # 确保正定

# 1. 特征值分解
eigenvalues, eigenvectors = np.linalg.eig(A)
print("特征值分解:")
print(f"特征值: {eigenvalues.round(4)}")
print(f"特征向量形状: {eigenvectors.shape}")

# 验证: A = V D V^-1
reconstructed = eigenvectors @ np.diag(eigenvalues) @ np.linalg.inv(eigenvectors)
print(f"重构误差: {np.linalg.norm(A - reconstructed):.6f}")

# 2. 奇异值分解（SVD）
U, S, Vt = np.linalg.svd(A)
print("\n奇异值分解:")
print(f"U 形状: {U.shape}")
print(f"奇异值: {S.round(4)}")
print(f"Vt 形状: {Vt.shape}")

# 验证: A = U S Vt
reconstructed = U @ np.diag(S) @ Vt
print(f"重构误差: {np.linalg.norm(A - reconstructed):.6f}")

# 低秩近似
k = 3  # 保留前3个奇异值
A_approx = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]
print(f"\n低秩近似误差 (k={k}): {np.linalg.norm(A - A_approx):.6f}")
```

### 线性方程组求解

```python
import numpy as np

# 求解 Ax = b
A = np.array([
    [3, 1, -1],
    [2, 4, 1],
    [-1, 2, 5]
])
b = np.array([4, 1, 1])

# 方法一：np.linalg.solve
x = np.linalg.solve(A, b)
print(f"解: {x}")
print(f"验证 Ax = b: {np.allclose(A @ x, b)}")

# 方法二：使用逆矩阵（不推荐，数值不稳定）
x2 = np.linalg.inv(A) @ b
print(f"逆矩阵法: {x2}")

# 方法三：最小二乘法（超定方程组）
A_over = np.random.rand(5, 3)
b_over = np.random.rand(5)
x_lstsq, residuals, rank, s = np.linalg.lstsq(A_over, b_over, rcond=None)
print(f"最小二乘解: {x_lstsq}")
```

---

## 本章小结

本章深入讲解了 NumPy 的核心操作：

1. **数组创建**：从列表转换、特殊数组、随机数组
2. **索引与切片**：基本索引、布尔索引、花式索引
3. **广播机制**：自动扩展不同形状数组进行运算
4. **向量化运算**：比循环快几个数量级，是高效代码的关键
5. **矩阵运算**：乘法、分解、方程求解

NumPy 是机器学习的基础工具，熟练掌握这些操作将大大提高编程效率。

下一章将展示线性代数在实际机器学习场景中的应用。