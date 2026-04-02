#!/usr/bin/env python3
"""
生成梯度方向示意图
直观展示"梯度指向函数值增长最快方向"的几何意义
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.size'] = 11

# 定义二元函数 f(x, y) = x^2 + y^2（一个碗状曲面）
def f(x, y):
    return x**2 + y**2

# 计算梯度
def gradient(x, y):
    return np.array([2*x, 2*y])

# 基准点
x0, y0 = 1.0, 0.5
z0 = f(x0, y0)
grad = gradient(x0, y0)

# 创建图形 - 两个子图
fig = plt.figure(figsize=(14, 6))

# ===== 子图1：山丘类比示意图 =====
ax1 = fig.add_subplot(121)

# 绘制等高线（代表山丘的地形图）
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

contour = ax1.contourf(X, Y, Z, levels=20, cmap='terrain', alpha=0.8)
ax1.contour(X, Y, Z, levels=20, colors='black', linewidths=0.5, alpha=0.5)

# 标记基准点
ax1.plot(x0, y0, 'ko', markersize=12, zorder=5, label='Your position')

# 绘制梯度向量（指向"上山"最快方向）
grad_norm = grad / np.linalg.norm(grad)  # 归一化
scale = 1.2  # 箭头长度
ax1.annotate('', xy=(x0 + scale*grad_norm[0], y0 + scale*grad_norm[1]),
             xytext=(x0, y0),
             arrowprops=dict(arrowstyle='->', color='red', lw=3),
             zorder=6)
ax1.text(x0 + 0.35, y0 + 0.75, 'Gradient direction\n(steepest ascent)', fontsize=11, color='red', ha='center')

# 绘制其他几个方向作对比
# 方向1：沿x轴
dir_x = np.array([1, 0])
dir_x_norm = dir_x / np.linalg.norm(dir_x)
ax1.annotate('', xy=(x0 + scale*dir_x_norm[0], y0 + scale*dir_x_norm[1]),
             xytext=(x0, y0),
             arrowprops=dict(arrowstyle='->', color='blue', lw=2, alpha=0.7))
ax1.text(x0 + 1.35, y0 + 0.15, 'East only', fontsize=9, color='blue')

# 方向2：沿y轴
dir_y = np.array([0, 1])
dir_y_norm = dir_y / np.linalg.norm(dir_y)
ax1.annotate('', xy=(x0 + scale*dir_y_norm[0], y0 + scale*dir_y_norm[1]),
             xytext=(x0, y0),
             arrowprops=dict(arrowstyle='->', color='green', lw=2, alpha=0.7))
ax1.text(x0 + 0.15, y0 + 1.35, 'North only', fontsize=9, color='green')

# 方向3：反梯度方向（下山最快）
ax1.annotate('', xy=(x0 - scale*grad_norm[0], y0 - scale*grad_norm[1]),
             xytext=(x0, y0),
             arrowprops=dict(arrowstyle='->', color='orange', lw=2.5))
ax1.text(x0 - 0.5, y0 - 0.75, 'Negative gradient\n(steepest descent)', fontsize=10, color='orange', ha='center')

# 标记最低点（山谷）
ax1.plot(0, 0, 'r*', markersize=15, label='Minimum (valley)')
ax1.text(0.1, -0.25, 'Minimum', fontsize=10, color='darkred', ha='center')

# 添加海拔标注
for level in [0.5, 1.0, 2.0, 4.0]:
    ax1.text(-1.8, np.sqrt(level-0.01), f'f={level}', fontsize=9, color='white')

ax1.set_xlabel('$x$ (East-West)', fontsize=12)
ax1.set_ylabel('$y$ (North-South)', fontsize=12)
ax1.set_title('Hill Terrain Analogy\nContour values = "altitude"', fontsize=13)
ax1.legend(loc='lower left', fontsize=10)
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)

# ===== 子图2：方向变化率对比图 =====
ax2 = fig.add_subplot(122)

# 计算不同角度的方向导数
angles = np.linspace(0, 2*np.pi, 100)
directional_derivatives = []

grad_magnitude = np.linalg.norm(grad)

for angle in angles:
    # 单位方向向量
    u = np.array([np.cos(angle), np.sin(angle)])
    # 方向导数 = 梯度 · 方向向量
    D_u = np.dot(grad, u)
    directional_derivatives.append(D_u)

directional_derivatives = np.array(directional_derivatives)

# 绘制方向导数随角度变化的曲线
ax2.plot(np.degrees(angles), directional_derivatives, 'b-', linewidth=2, label='Directional derivative $D_{\\mathbf{u}} f$')

# 标记关键点
# 最大值：梯度方向
grad_angle = np.arctan2(grad[1], grad[0])
grad_angle_deg = np.degrees(grad_angle)
ax2.plot(grad_angle_deg, grad_magnitude, 'ro', markersize=12, zorder=5)
ax2.annotate(f'Maximum\n$D_u f = {grad_magnitude:.2f}$\n(Gradient direction)',
             xy=(grad_angle_deg, grad_magnitude),
             xytext=(grad_angle_deg+30, grad_magnitude+0.4),
             fontsize=10, color='red',
             arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

# 最小值：负梯度方向
ax2.plot(grad_angle_deg + 180, -grad_magnitude, 'go', markersize=12, zorder=5)
ax2.annotate(f'Minimum\n$D_u f = {-grad_magnitude:.2f}$\n(Negative gradient)',
             xy=(grad_angle_deg + 180, -grad_magnitude),
             xytext=(grad_angle_deg + 150, -grad_magnitude - 0.6),
             fontsize=10, color='green',
             arrowprops=dict(arrowstyle='->', color='green', lw=1.5))

# 零值：与梯度垂直的方向
ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax2.plot(grad_angle_deg + 90, 0, 'mo', markersize=8, zorder=5)
ax2.plot(grad_angle_deg + 270, 0, 'mo', markersize=8, zorder=5)
ax2.text(grad_angle_deg + 110, 0.15, 'Contour direction\n(no change)', fontsize=9, color='purple')

# 填充正负区域
ax2.fill_between(np.degrees(angles), 0, directional_derivatives,
                  where=(directional_derivatives > 0), color='red', alpha=0.2, label='Function increases')
ax2.fill_between(np.degrees(angles), 0, directional_derivatives,
                  where=(directional_derivatives < 0), color='green', alpha=0.2, label='Function decreases')

# 添加公式说明
grad_str = f'({grad[0]:.1f}, {grad[1]:.1f})'
textstr = (f'Formula: $D_{{\\mathbf{{u}}}} f = \\nabla f \\cdot \\mathbf{{u}}$\n'
           f'$= ||\\nabla f|| \\cos\\theta$\n\n'
           f'Point: $(x_0, y_0) = ({x0}, {y0})$\n'
           f'Gradient: $\\nabla f = {grad_str}$\n'
           f'Magnitude: $||\\nabla f|| = {grad_magnitude:.2f}$')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=10,
         verticalalignment='top', bbox=props)

ax2.set_xlabel('Direction angle $\\theta$ (degrees)', fontsize=12)
ax2.set_ylabel('Directional derivative $D_{\\mathbf{u}} f$', fontsize=12)
ax2.set_title('Rate of Change in Different Directions\nGradient direction has maximum rate', fontsize=13)
ax2.legend(loc='lower right', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 360)
ax2.set_ylim(-grad_magnitude * 1.5, grad_magnitude * 1.5)

plt.tight_layout()
plt.savefig('/root/devspaces/ideaspaces/docs/calculus/assets/gradient_direction.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("图片已保存至 docs/calculus/assets/gradient_direction.png")