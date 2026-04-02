#!/usr/bin/env python3
"""
生成梯度方向的三维示意图
展示函数 f(x, y) = x^2 + y^2 的曲面及梯度方向
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11

# 定义二元函数 f(x, y) = x^2 + y^2（碗状曲面）
def f(x, y):
    return x**2 + y**2

# 计算梯度
def gradient(x, y):
    return np.array([2*x, 2*y])

# 基准点
x0, y0 = 1.0, 0.5
z0 = f(x0, y0)
grad = gradient(x0, y0)  # (2, 1)

# 创建曲面数据
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# 创建图形
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# 绘制曲面
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7, linewidth=0, antialiased=True)

# 绘制等高线（在底部投影）
ax.contour(X, Y, Z, levels=10, colors='gray', linewidths=0.5, linestyles='solid', offset=0)

# 标记基准点 (1, 0.5, f(1, 0.5))
ax.scatter([x0], [y0], [z0], color='black', s=100, marker='o', label='Point (1, 0.5)', zorder=10)

# 绘制梯度向量（在曲面上方）
grad_norm = grad / np.linalg.norm(grad)  # 归一化
scale = 1.5  # 箭头长度
# 梯度方向箭头 - 从基准点向上延伸
ax.quiver(x0, y0, z0 + 0.5, grad_norm[0], grad_norm[1], 0,
          color='red', arrow_length_ratio=0.2, linewidth=3, label='Gradient direction')

# 绘制负梯度方向
ax.quiver(x0, y0, z0 + 0.5, -grad_norm[0], -grad_norm[1], 0,
          color='orange', arrow_length_ratio=0.2, linewidth=2.5, label='Negative gradient')

# 绘制与梯度垂直的方向 (1, -2) 归一化
perp = np.array([1, -2])
perp_norm = perp / np.linalg.norm(perp)
ax.quiver(x0, y0, z0 + 0.5, perp_norm[0], perp_norm[1], 0,
          color='purple', arrow_length_ratio=0.2, linewidth=2, label='Perpendicular to gradient')

# 绘制从基准点到最低点的路径线（负梯度方向）
ax.plot([x0, x0 - 2*grad_norm[0]], [y0, y0 - 2*grad_norm[1]], [z0, f(x0 - 2*grad_norm[0], y0 - 2*grad_norm[1])],
        'g--', linewidth=2, alpha=0.7)

# 标记最低点
ax.scatter([0], [0], [0], color='red', s=150, marker='*', label='Minimum (0, 0)', zorder=10)

# 添加颜色条
cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, pad=0.1)
cbar.set_label('Function value $f(x, y) = x^2 + y^2$', fontsize=11)

# 设置坐标轴标签
ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('$y$', fontsize=12)
ax.set_zlabel('$f(x, y)$', fontsize=12)

# 设置标题
ax.set_title('3D View: Gradient Points to Steepest Ascent\n$f(x, y) = x^2 + y^2$ at point $(1, 0.5)$', fontsize=14)

# 设置视角
ax.view_init(elev=25, azim=45)

# 设置坐标范围
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(0, 5)

# 添加图例（放在右上角）
ax.legend(loc='upper right', fontsize=10)

# 添加文字说明框（放在左下角）
textstr = (f'Point: $(1, 0.5)$\n'
           f'$f(1, 0.5) = {z0:.2f}$\n'
           f'Gradient: $\\nabla f = (2, 1)$\n'
           f'$||\\nabla f|| = \\sqrt{{5}} \\approx 2.24$')

props = dict(boxstyle='round', facecolor='white', alpha=0.9)
ax.text2D(0.02, 0.15, textstr, transform=ax.transAxes, fontsize=11,
          verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('/root/devspaces/ideaspaces/docs/calculus/assets/gradient_3d.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("图片已保存至 docs/calculus/assets/gradient_3d.png")