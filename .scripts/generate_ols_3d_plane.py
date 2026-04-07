import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font = FontProperties(fname=font_path)

# 创建图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 只用1个样本点来展示
# 设定回归平面参数
beta0 = 50  # 截距
beta1 = 2   # 面积系数
beta2 = 10  # 卧室系数

# 一个样本点：面积=120，卧室=3，真实房价=300
x1 = 120  # 面积
x2 = 3    # 卧室数
y_real = 310  # 真实房价（略高于预测值，便于展示残差）

# 预测值（平面上的点）
y_pred = beta0 + beta1 * x1 + beta2 * x2  # = 50 + 240 + 30 = 320

# 残差
residual = y_real - y_pred  # = -10

# 创建回归平面（小范围，便于看清）
area_grid = np.linspace(100, 140, 10)
bedroom_grid = np.linspace(2, 4, 10)
Area_Grid, Bedroom_Grid = np.meshgrid(area_grid, bedroom_grid)
Price_Grid = beta0 + beta1 * Area_Grid + beta2 * Bedroom_Grid

# 绘制回归平面
ax.plot_surface(Area_Grid, Bedroom_Grid, Price_Grid, alpha=0.4,
                color='#1f77b4', edgecolor='#1f77b4', linewidth=0.5)

# 绘制真实样本点
ax.scatter([x1], [x2], [y_real], c='#2ca02c', s=150, alpha=0.9,
           label='样本点（真实值）', depthshade=False)

# 绘制预测点（平面上的投影点）
ax.scatter([x1], [x2], [y_pred], c='#1f77b4', s=100, alpha=0.7,
           label='预测点（平面上）', depthshade=False)

# 绘制残差线（从真实点到平面的垂直线）
ax.plot([x1, x1], [x2, x2], [y_real, y_pred],
        'r-', linewidth=3, alpha=0.9, label='残差')

# 绘制辅助线：从预测点到x1轴的垂线
ax.plot([x1, x1], [x2, x2], [y_pred, 250], 'gray', linewidth=1, alpha=0.5, linestyle='--')

# 在x1-x2平面上标注投影位置
ax.scatter([x1], [x2], [250], c='gray', s=50, alpha=0.5, marker='x')
ax.plot([x1, x1], [x2-0.3, x2+0.3], [250, 250], 'gray', linewidth=1, alpha=0.3)
ax.plot([x1-10, x1+10], [x2, x2], [250, 250], 'gray', linewidth=1, alpha=0.3)

# 标注文字
ax.text(x1+5, x2, y_real+5, '真实值 y', fontproperties=font, fontsize=11, color='#2ca02c')
ax.text(x1+5, x2, y_pred-10, '预测值 ŷ', fontproperties=font, fontsize=11, color='#1f77b4')
ax.text(x1-15, x2, (y_real+y_pred)/2, '残差 e', fontproperties=font, fontsize=11, color='#d62728')

# 设置坐标轴
ax.set_xlabel('特征 $x_1$（面积）', fontproperties=font, fontsize=12, labelpad=10)
ax.set_ylabel('特征 $x_2$（卧室数）', fontproperties=font, fontsize=12, labelpad=10)
ax.set_zlabel('结果 $y$（房价）', fontproperties=font, fontsize=12, labelpad=10)

# 设置标题
ax.set_title('线性回归：一个样本的残差', fontproperties=font, fontsize=14, fontweight='bold')

# 设置坐标范围（放大展示）
ax.set_xlim(100, 140)
ax.set_ylim(2, 4)
ax.set_zlim(250, 330)

# 设置视角
ax.view_init(elev=20, azim=30)

# 添加图例
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#2ca02c',
           markersize=12, label='真实值 y'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#1f77b4',
           markersize=10, label='预测值 ŷ（在平面上）'),
    Line2D([0], [0], color='#d62728', linewidth=3, label='残差 e = y - ŷ'),
    Line2D([0], [0], color='#1f77b4', linewidth=5, alpha=0.5, label='回归平面'),
]
ax.legend(handles=legend_elements, prop=font, loc='upper right', fontsize=10)

# 添加说明
ax.text2D(0.02, 0.02, '残差 = 真实值 - 平面预测值\nOLS 最小化所有残差的平方和',
          transform=ax.transAxes, fontproperties=font, fontsize=10,
          color='#666666', style='italic')

plt.tight_layout()
plt.savefig('docs/statistical-learning/linear-models/assets/ols-3d-plane.png',
            dpi=150, bbox_inches='tight', facecolor='white')
print("图片已更新")