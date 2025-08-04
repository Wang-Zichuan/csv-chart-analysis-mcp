import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
from typing import Dict, Any

def generate_scatter_plot(
    csv_path: str,
    x_column: str,
    y_column: str,
    save_dir: str = "./charts"
) -> Dict[str, Any]:
    """
    从CSV文件中读取指定列数据，生成散点图并计算相关系数

    参数:
        csv_path: CSV文件路径
        x_column: 用作x轴的列名
        y_column: 用作y轴的列名
        save_dir: 图片保存目录，默认为'./charts'

    返回:
        包含图表路径、相关系数和统计信息的字典
    """
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_path)
        
        # 检查列是否存在
        if x_column not in df.columns:
            return {"error": f"列 '{x_column}' 不存在于CSV文件中", "success": False}
        if y_column not in df.columns:
            return {"error": f"列 '{y_column}' 不存在于CSV文件中", "success": False}
        
        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)
        
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 获取文件名用于命名
        file_name = os.path.splitext(os.path.basename(csv_path))[0]
        save_path = os.path.join(save_dir, f'{file_name}_{x_column}_{y_column}_scatter.png')
        
        # 创建散点图
        plt.figure(figsize=(10, 8))
        
        # 绘制散点图
        plt.scatter(df[x_column], df[y_column], alpha=0.6)
        
        # 添加趋势线
        z = np.polyfit(df[x_column], df[y_column], 1)
        p = np.poly1d(z)
        plt.plot(df[x_column], p(df[x_column]), "r--", alpha=0.8)
        
        # 计算相关系数
        pearson_corr, pearson_p = stats.pearsonr(df[x_column], df[y_column])
        spearman_corr, spearman_p = stats.spearmanr(df[x_column], df[y_column])
        
        # 添加标题和标签
        plt.title(f'{x_column} vs {y_column}\n皮尔逊相关系数: {pearson_corr:.3f} (p={pearson_p:.3f})')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        
        # 添加网格
        plt.grid(True, alpha=0.3)
        
        # 保存图表
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 返回结果
        return {
            "success": True,
            "plot_path": save_path,
            "pearson_correlation": float(pearson_corr),
            "pearson_p_value": float(pearson_p),
            "spearman_correlation": float(spearman_corr),
            "spearman_p_value": float(spearman_p),
            "sample_size": len(df)
        }
        
    except Exception as e:
        return {"error": str(e), "success": False}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        result = generate_scatter_plot(sys.argv[1], sys.argv[2], sys.argv[3])
        print(result)
    else:
        print("用法: python 多变量相关性.py <csv文件路径> <x列名> <y列名>")