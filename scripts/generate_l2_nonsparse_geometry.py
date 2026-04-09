"""
生成 L2 单位球与损失函数等值线相交的几何解释图片
用于文档 docs/statistical-learning/linear-models/regularization-glm.md
展示 L2 正则化不会产生稀疏解：等值线碰到圆边，参数不为零
"""

import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


def l2_unit_ball(t=1.0, n_points=200):
    """
    生成 L2 单位球（圆形）边界点
    参数 t 控制圆的大小：β₁² + β₂² ≤ t
    """
    theta = np.linspace(0, 2*np.pi, n_points)
    r = np.sqrt(t)  # 半径
    x = r * np.cos(theta)
    y = r * np.sin(theta)
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

# L2 单位球参数 t（半径平方）
t = 1.0
r = np.sqrt(t)  # 半径

# 绘制 L2 单位球（圆形）
x_l2, y_l2 = l2_unit_ball(t)
ax.fill(x_l2, y_l2, color='steelblue', alpha=0.3, label='L2 约束区域')
ax.plot(x_l2, y_l2, color='steelblue', linewidth=2)

# 未正则化的最优解位置（椭圆中心）
# 设置在第一象限，使等值线向左下方扩展时碰到圆形边界
center_x = 2.0  # β₁ 方向偏移
center_y = 1.5  # β₂ 方向偏移

# 椭圆形状：a/b 比例
ratio = 1.5  # a > b，椭圆在 β₁ 方向更宽

# 计算让椭圆刚好与圆形边界相切的参数
# 圆心在原点，半径 r
# 椭圆中心在 (center_x, center_y)，半轴 a, b (a = ratio * b)
# 相切条件：椭圆上的点到原点的最小距离等于 r
# 这是一个几何优化问题，我们用数值方法求解

# 椭圆方程: x = center_x + a*cos(θ), y = center_y + b*sin(θ)
# 到原点距离: d² = (center_x + a*cos(θ))² + (center_y + b*sin(θ))²
# 最小化 d² 关于 θ

from scipy.optimize import minimize_scalar

def min_dist_to_origin(a, b, cx, cy):
    """计算椭圆到原点的最小距离"""
    def dist_sq(theta):
        x = cx + a * np.cos(theta)
        y = cy + b * np.sin(theta)
        return x**2 + y**2
    result = minimize_scalar(dist_sq)
    return np.sqrt(result.x), result.fun  # 返回最优theta和最小距离平方

# 通过调整 a 使椭圆刚好与圆相切
# 最小距离 = r

def find_tangent_a(r, ratio, cx, cy):
    """找到使椭圆与圆相切的 a 值"""
    # 初始猜测
    a_init = r * 1.5

    def objective(a):
        b = a / ratio
        _, min_dist_sq = min_dist_to_origin(a, b, cx, cy)
        return min_dist_sq - r**2  # 目标：最小距离平方 = r²

    # 简单搜索（因为函数单调）
    # 当 a 增大时，椭圆变大，最小距离减小
    a_low = 0.1
    a_high = 3.0

    for _ in range(50):
        a_mid = (a_low + a_high) / 2
        val = objective(a_mid)
        if abs(val) < 0.001:
            break
        if val > 0:  # 距离太大，需要更大的椭圆
            a_low = a_mid
        else:  # 距离太小，需要更小的椭圆
            a_high = a_mid

    return a_mid

a_contact = find_tangent_a(r, ratio, center_x, center_y)
b_contact = a_contact / ratio

# 找到相切点的位置
theta_opt, _ = min_dist_to_origin(a_contact, b_contact, center_x, center_y)
contact_x = center_x + a_contact * np.cos(theta_opt)
contact_y = center_y + b_contact * np.sin(theta_opt)

# 绘制较小的等值线（不接触圆形）
for scale in [0.3, 0.5, 0.7]:
    a = a_contact * scale
    b = a / ratio
    x_c, y_c = loss_contour(center_x, center_y, a, b)
    ax.plot(x_c, y_c, color='orange', linewidth=1.5, linestyle='--', alpha=0.6)

# 绘制刚好接触圆边的等值线（重点展示）
x_contact, y_contact = loss_contour(center_x, center_y, a_contact, b_contact)
ax.plot(x_contact, y_contact, color='red', linewidth=2.5, label='损失等值线')

# 标记最优解位置（圆边上的切点）
ax.plot(contact_x, contact_y, 'ro', markersize=12, label='最优解')
ax.annotate(f'β₁ ≈ {contact_x:.1f}\nβ₂ ≈ {contact_y:.1f}',
            xy=(contact_x, contact_y), xytext=(contact_x+0.25, contact_y+0.35),
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
ax.set_title('L2 正则化的几何解释\n等值线碰到光滑圆边 → 非稀疏解', fontsize=14)
ax.legend(loc='upper right', fontsize=10)

# 添加说明文字
ax.text(0.1, 1.8,
        '约束区域：β₁² + β₂² ≤ t\n'
        '圆形边界处处光滑\n'
        '→ 两个参数都不为零',
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# 保存图片
output_path = '/root/devspaces/ideaspaces/docs/statistical-learning/linear-models/assets/l2_nonsparse_geometry.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"图片已保存到: {output_path}")