#!/usr/bin/env python3
"""
生成向量内积（点积）几何含义示意图
用于线性代数系列文章第1章：引言
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置字体
plt.rcParams['axes.unicode_minus'] = False

# 创建图形，使用3个子图
fig, axes = plt.subplots(1, 3, figsize=(14, 5), dpi=150)

# 共同的向量 u（用于所有子图）
u = np.array([2.5, 0])
origin = np.array([0, 0])

# 三个不同的向量 v，展示不同的夹角
scenarios = [
    {'v': np.array([2, 0]), 'title': 'Same Direction\n(θ = 0°, dot product > 0)', 'color': '#27AE60'},
    {'v': np.array([0, 2]), 'title': 'Orthogonal\n(θ = 90°, dot product = 0)', 'color': '#F39C12'},
    {'v': np.array([-2, 0]), 'title': 'Opposite Direction\n(θ = 180°, dot product < 0)', 'color': '#E74C3C'}
]

for idx, (ax, scenario) in enumerate(zip(axes, scenarios)):
    v = scenario['v']

    # 绘制坐标轴
    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='-')
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='-')

    # 绘制向量 u（蓝色）
    ax.annotate('', xy=u, xytext=origin,
                arrowprops=dict(arrowstyle='->', color='#2E86AB', lw=3))

    # 绘制向量 v（根据场景不同颜色）
    ax.annotate('', xy=v, xytext=origin,
                arrowprops=dict(arrowstyle='->', color=scenario['color'], lw=3))

    # 标记向量
    ax.text(u[0] + 0.2, u[1] - 0.3, r'$\mathbf{u}$', fontsize=14, color='#2E86AB', fontweight='bold')
    ax.text(v[0] + 0.15, v[1] + 0.15, r'$\mathbf{v}$', fontsize=14, color=scenario['color'], fontweight='bold')

    # 标记原点
    ax.plot(0, 0, 'o', color='black', markersize=4)

    # 设置坐标轴
    ax.set_xlim(-3, 3.5)
    ax.set_ylim(-0.5, 3)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle=':')
    ax.set_xlabel('x', fontsize=11)
    if idx == 0:
        ax.set_ylabel('y', fontsize=11)

    # 设置标题
    ax.set_title(scenario['title'], fontsize=11, pad=4)

plt.suptitle('Geometric Meaning of Dot Product', fontsize=13, y=0.94)
plt.tight_layout()
plt.subplots_adjust(top=0.72, hspace=0.3)

# 保存图片
plt.savefig('/root/devspaces/ideaspaces/articles/linear-algebra-vectors-matrices/draft/assets/vector_dot_product.png',
            dpi=150, bbox_inches='tight', facecolor='white')
print("向量内积示意图已保存到: assets/vector_dot_product.png")

plt.close()
