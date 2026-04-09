"""
生成 L1 单位球与损失函数等值线相交的几何解释图片
用于文档 docs/statistical-learning/linear-models/regularization-glm.md
展示稀疏解的几何来源：等值线碰到菱形顶点产生稀疏解
"""

import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


def l1_unit_ball(t=1.0):
    """
    生成 L1 单位球（菱形）边界点
    参数 t 控制菱形大小：|β₁| + |β₂| ≤ t
    """
    x = np.array([0, t, 0, -t, 0])
    y = np.array([t, 0, -t, 0, t])
    return x, y


def loss_contour(center_x, center_y, a, b, n_points=200):
    """
    生成损失函数等值线（椭圆形）
    参数 center: 等值线中心（未正则化时的最优解）
    参数 a, b: 椭圆的两个半轴长度
    """
    theta = np.linspace(0, 2*np.pi, n_points)
    x = center_x + a * np.cos(theta)
    y = center_y + b * np.sin(theta)
    return x, y


# 创建图形
fig, ax = plt.subplots(figsize=(8, 8))

# L1 单位球参数 t
t = 1.0

# 绘制 L1 单位球（菱形）
x_l1, y_l1 = l1_unit_ball(t)
ax.fill(x_l1, y_l1, color='steelblue', alpha=0.3, label='L1 约束区域')
ax.plot(x_l1, y_l1, color='steelblue', linewidth=2)

# 未正则化的最优解位置（椭圆中心）
# 设置在第一象限，使等值线向左下方扩展时碰到菱形顶点
center_x = 2.0  # β₁ 方向偏移
center_y = 1.5  # β₂ 方向偏移

# 绘制多条损失函数等值线（椭圆形）
# 从小到大扩展，直到碰到菱形顶点
# 椭圆形状：假设 β₂ 方向的损失更敏感（椭圆在该方向更窄）

# 计算第一条碰到顶点 (t, 0) 的等值线参数
# 椭圆方程: ((x - center_x)/a)^2 + ((y - center_y)/b)^2 = 1
# 顶点 (t, 0) 在椭圆上: ((t - center_x)/a)^2 + ((0 - center_y)/b)^2 = 1
# 需要计算合适的 a, b 使得椭圆刚好通过 (t, 0)

# 设定 a/b 的比例（椭圆形状）
ratio = 1.5  # a > b，椭圆在 β₁ 方向更宽

# 计算让椭圆通过 (t, 0) 的 a 值
# ((t - center_x)/a)^2 + (-center_y)/(a/ratio))^2 = 1
# ((t - center_x)^2 + center_y^2 * ratio^2) / a^2 = 1
# a = sqrt((t - center_x)^2 + center_y^2 * ratio^2)
a_contact = np.sqrt((t - center_x)**2 + center_y**2 * ratio**2)
b_contact = a_contact / ratio

# 绘制较小的等值线（不接触菱形）
for scale in [0.3, 0.5, 0.7]:
    a = a_contact * scale
    b = a / ratio
    x_c, y_c = loss_contour(center_x, center_y, a, b)
    ax.plot(x_c, y_c, color='orange', linewidth=1.5, linestyle='--', alpha=0.6)

# 绘制刚好接触顶点的等值线（重点展示）
x_contact, y_contact = loss_contour(center_x, center_y, a_contact, b_contact)
ax.plot(x_contact, y_contact, color='red', linewidth=2.5, label='损失等值线')

# 标记最优解位置（菱形顶点）
ax.plot(t, 0, 'ro', markersize=12, label='最优解 (稀疏点)')
ax.annotate('β₁ = t\nβ₂ = 0', xy=(t, 0), xytext=(t+0.25, 0.35),
            fontsize=11, ha='left', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5))

# 标记未正则化最优解
ax.plot(center_x, center_y, 'ko', markersize=10, label='未正则化最优解')
ax.annotate('无约束\n最优解', xy=(center_x, center_y), xytext=(center_x+0.15, center_y+0.1),
            fontsize=10, ha='left')

# 绘制坐标轴
ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--')
ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--')

# 设置图形属性
ax.set_xlim(-0.5, 3.0)
ax.set_ylim(-0.5, 2.2)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)

# 添加标签和标题
ax.set_xlabel('β₁', fontsize=14)
ax.set_ylabel('β₂', fontsize=14)
ax.set_title('L1 正则化的几何解释\n等值线首次碰到菱形顶点 → 稀疏解', fontsize=14)
ax.legend(loc='upper right', fontsize=10)

# 添加说明文字
ax.text(0.1, 1.8,
        '约束区域：|β₁| + |β₂| ≤ t\n'
        '等值线扩展 → 碰到顶点\n'
        '→ β₂ = 0（稀疏解）',
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# 保存图片
output_path = '/root/devspaces/ideaspaces/docs/statistical-learning/linear-models/assets/l1_sparse_geometry.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"图片已保存到: {output_path}")