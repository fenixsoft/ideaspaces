#!/usr/bin/env python3
"""
生成偏导数几何意义示意图
展示二元函数曲面与截平面交线的切线斜率
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11

# 定义二元函数 f(x, y) = x² + y²
def f(x, y):
    return x**2 + y**2

# 基准点
x0, y0 = 1.0, 1.0
z0 = f(x0, y0)

# 创建图形 - 两个子图：整体曲面视角和截面视角
fig = plt.figure(figsize=(14, 6))

# ===== 子图1：整体曲面与截平面 =====
ax1 = fig.add_subplot(121, projection='3d')

# 创建网格
x = np.linspace(-1.5, 1.5, 100)
y = np.linspace(-1.5, 1.5, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# 绘制曲面
ax1.plot_surface(X, Y, Z, alpha=0.7, cmap='coolwarm', edgecolor='none')

# 绘制截平面 y = y0 (半透明平面)
Y_plane = np.full_like(X, y0)
ax1.plot_surface(X, Y_plane, Z, alpha=0.3, color='yellow', edgecolor='none')

# 截平面与曲面的交线 (沿 x 方向)
x_curve = np.linspace(-1.5, 1.5, 100)
z_curve = f(x_curve, y0)
ax1.plot(x_curve, np.full_like(x_curve, y0), z_curve, 'r-', linewidth=3, label='Section curve: $y = y_0$')

# 在基准点绘制切线
# 偏导数 ∂f/∂x = 2x，在 (x0, y0) 处为 2x0 = 2
partial_fx = 2 * x0  # = 2

# 切线参数 (沿 x 方向)
t = np.linspace(-0.5, 0.5, 50)
x_tangent = x0 + t
y_tangent = np.full_like(t, y0)
z_tangent = z0 + partial_fx * t
ax1.plot(x_tangent, y_tangent, z_tangent, 'g-', linewidth=3, label='Tangent line')

# 标记基准点
ax1.scatter([x0], [y0], [z0], color='black', s=100, marker='o', label='Point $(x_0, y_0, f(x_0,y_0))$')

# 设置标签和标题
ax1.set_xlabel('$x$', fontsize=12)
ax1.set_ylabel('$y$', fontsize=12)
ax1.set_zlabel('$z$', fontsize=12)
ax1.set_title('Surface and Section Plane $y = y_0$', fontsize=13)
ax1.legend(loc='upper left', fontsize=9)

# 设置视角
ax1.view_init(elev=25, azim=-60)

# ===== 子图2：截面视角（2D投影） =====
ax2 = fig.add_subplot(122)

# 绘制截面曲线 z = f(x, y0) = x² + y0²
x_2d = np.linspace(-1.5, 1.5, 100)
z_2d = f(x_2d, y0)
ax2.plot(x_2d, z_2d, 'b-', linewidth=2.5, label='Section: $z = f(x, y_0) = x^2 + y_0^2$')

# 绘制切线
z_tangent_2d = z0 + partial_fx * t
ax2.plot(x_tangent, z_tangent_2d, 'g-', linewidth=2.5, label='Tangent: slope = $\\frac{\\partial f}{\\partial x} = 2x_0$')

# 标记基准点
ax2.plot(x0, z0, 'ko', markersize=10, zorder=5)
ax2.annotate('$(x_0, f(x_0, y_0))$', xy=(x0, z0), xytext=(x0+0.15, z0-0.3), fontsize=11)

# 绘制斜率示意
# 在切线上取两点展示斜率
dx_demo = 0.3
ax2.annotate('', xy=(x0+dx_demo, z0+partial_fx*dx_demo), xytext=(x0, z0),
             arrowprops=dict(arrowstyle='->', color='green', lw=2))
ax2.text(x0+0.1, z0+0.8, f'slope = {partial_fx:.1f}', fontsize=12, color='green')

# 添加标注说明
textstr = (f'Function: $z = f(x,y) = x^2 + y^2$\n'
           f'Section plane: $y = y_0 = {y0:.1f}$\n'
           f'Section curve: $z = x^2 + {y0**2:.1f}$\n'
           f'Partial derivative:\n  $\\frac{{\\partial f}}{{\\partial x}} = 2x_0 = {partial_fx:.1f}$')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
ax2.text(0.98, 0.02, textstr, transform=ax2.transAxes, fontsize=10,
         verticalalignment='bottom', horizontalalignment='right', bbox=props)

# 设置标签和标题
ax2.set_xlabel('$x$ (with $y = y_0$ fixed)', fontsize=12)
ax2.set_ylabel('$z$', fontsize=12)
ax2.set_title('Section Curve and Tangent\n(Geometric meaning of $\\partial f/\\partial x$)', fontsize=13)
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(0, 5)

plt.tight_layout()
plt.savefig('/root/devspaces/ideaspaces/docs/calculus/assets/partial_derivative_geometry.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("图片已保存至 docs/calculus/assets/partial_derivative_geometry.png")