#!/usr/bin/env python3
"""
生成向量加法平行四边形法则示意图
用于线性代数系列文章第1章：引言
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置字体
plt.rcParams['axes.unicode_minus'] = False

# 创建图形
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

# 定义向量
u = np.array([3, 1])    # 向量 u
v = np.array([1, 2])    # 向量 v
origin = np.array([0, 0])

# 计算向量和
u_plus_v = u + v        # (4, 3)

# 绘制坐标轴
ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='-')
ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='-')

# 绘制向量 u（从原点出发）
ax.annotate('', xy=u, xytext=origin,
            arrowprops=dict(arrowstyle='->', color='#2E86AB', lw=2.5))

# 绘制向量 v（从原点出发）
ax.annotate('', xy=v, xytext=origin,
            arrowprops=dict(arrowstyle='->', color='#A23B72', lw=2.5))

# 绘制向量 v 从向量 u 的终点出发（平行四边形的另一条边）
ax.annotate('', xy=u_plus_v, xytext=u,
            arrowprops=dict(arrowstyle='->', color='#A23B72', lw=2, linestyle='--'))

# 绘制向量 u 从向量 v 的终点出发（平行四边形的另一条边）
ax.annotate('', xy=u_plus_v, xytext=v,
            arrowprops=dict(arrowstyle='->', color='#2E86AB', lw=2, linestyle='--'))

# 绘制向量和 u+v（对角线）
ax.annotate('', xy=u_plus_v, xytext=origin,
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=3))

# 标记各个点
ax.plot(*u, 'o', color='#2E86AB', markersize=6)
ax.plot(*v, 'o', color='#A23B72', markersize=6)
ax.plot(*u_plus_v, 'o', color='#E74C3C', markersize=6)

# 添加标签
ax.text(u[0] + 0.2, u[1] - 0.3, r'$\mathbf{u}$', fontsize=14, color='#2E86AB', fontweight='bold')
ax.text(v[0] - 0.3, v[1] + 0.2, r'$\mathbf{v}$', fontsize=14, color='#A23B72', fontweight='bold')
ax.text(u_plus_v[0] + 0.2, u_plus_v[1] + 0.1, r'$\mathbf{u} + \mathbf{v}$', fontsize=14, color='#E74C3C', fontweight='bold')

# 设置坐标轴标签
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)

# 设置坐标轴范围
ax.set_xlim(-0.5, 5)
ax.set_ylim(-0.5, 4)

# 设置等比例
ax.set_aspect('equal')

# 添加网格
ax.grid(True, alpha=0.3, linestyle=':')

# 设置标题
ax.set_title('Parallelogram Law of Vector Addition', fontsize=14, pad=15)

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('/root/devspaces/ideaspaces/articles/linear-algebra-vectors-matrices/draft/assets/vector_addition.png',
            dpi=150, bbox_inches='tight', facecolor='white')
print("向量加法示意图已保存到: assets/vector_addition.png")

plt.close()
