import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from typing import Dict, Any, Optional, Tuple

def generate_scatter_plot_advanced(
    csv_path: str,
    x_column: str,
    y_column: str,
    hue_column: Optional[str] = None,
    style_column: Optional[str] = None,
    save_dir: str = "./charts",
    figsize: Tuple[int, int] = (10, 8),
    alpha: float = 0.6,
    add_regression: bool = True,
    point_size: int = 50
) -> Dict[str, Any]:
    """
    生成高级散点图，支持分组、样式和回归线

    参数:
        csv_path: CSV文件路径
        x_column: 用作x轴的列名
        y_column: 用作y轴的列名
        hue_column: 用于颜色分组的列名（可选）
        style_column: 用于样式分组的列名（可选）
        save_dir: 图片保存目录，默认为'./charts'
        figsize: 图形尺寸，默认为(10, 8)
        alpha: 点的透明度，默认为0.6
        add_regression: 是否添加回归线，默认为True
        point_size: 点的大小，默认为50

    返回:
        包含图表路径和统计信息的字典
    """
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_path)
        
        # 检查必需列是否存在
        required_columns = [x_column, y_column]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return {"error": f"列 {missing_columns} 不存在于CSV文件中", "success": False}
        
        # 检查可选列
        if hue_column and hue_column not in df.columns:
            return {"error": f"颜色分组列 '{hue_column}' 不存在于CSV文件中", "success": False}
        
        if style_column and style_column not in df.columns:
            return {"error": f"样式分组列 '{style_column}' 不存在于CSV文件中", "success": False}
        
        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)
        
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 获取文件名用于命名
        file_name = os.path.splitext(os.path.basename(csv_path))[0]
        
        # 创建散点图
        plt.figure(figsize=figsize)
        
        # 使用seaborn创建散点图
        scatter = sns.scatterplot(
            data=df,
            x=x_column,
            y=y_column,
            hue=hue_column,
            style=style_column,
            alpha=alpha,
            s=point_size
        )
        
        # 添加回归线（如果启用）
        if add_regression:
            sns.regplot(
                data=df,
                x=x_column,
                y=y_column,
                scatter=False,
                color='red',
                line_kws={'linestyle': '--', 'alpha': 0.8}
            )
        
        # 计算相关系数
        valid_data = df[[x_column, y_column]].dropna()
        pearson_corr = valid_data[x_column].corr(valid_data[y_column])
        
        # 添加标题和标签
        title = f'{x_column} vs {y_column}'
        if hue_column:
            title += f' (按{hue_column}分组)'
        
        plt.title(f'{title}\n相关系数: {pearson_corr:.3f}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        
        # 添加网格
        plt.grid(True, alpha=0.3)
        
        # 保存图表
        save_path = os.path.join(save_dir, f'{file_name}_{x_column}_{y_column}_scatter_advanced.png')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 计算分组统计（如果有分组变量）
        group_stats = {}
        if hue_column:
            grouped = df.groupby(hue_column)
            group_stats = {
                group: {
                    'count': len(data),
                    'x_mean': data[x_column].mean(),
                    'y_mean': data[y_column].mean(),
                    'correlation': data[x_column].corr(data[y_column])
                }
                for group, data in grouped
            }
        
        # 计算总体统计
        overall_stats = {
            'total_points': len(df),
            'correlation': pearson_corr,
            'x_range': [df[x_column].min(), df[x_column].max()],
            'y_range': [df[y_column].min(), df[y_column].max()],
            'missing_values': df[[x_column, y_column]].isnull().sum().to_dict()
        }
        
        return {
            "success": True,
            "plot_path": save_path,
            "correlation": float(pearson_corr),
            "group_statistics": group_stats,
            "overall_statistics": overall_stats,
            "columns_used": [x_column, y_column, hue_column, style_column]
        }
        
    except Exception as e:
        return {"error": str(e), "success": False}

def generate_pairplot(
    csv_path: str,
    numeric_columns: list,
    hue_column: Optional[str] = None,
    save_dir: str = "./charts"
) -> Dict[str, Any]:
    """
    生成数值变量的配对图矩阵

    参数:
        csv_path: CSV文件路径
        numeric_columns: 要分析的数值列名列表
        hue_column: 用于颜色分组的列名（可选）
        save_dir: 图片保存目录，默认为'./charts'

    返回:
        包含图表路径的字典
    """
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_path)
        
        # 检查列是否存在
        missing_columns = [col for col in numeric_columns if col not in df.columns]
        if missing_columns:
            return {"error": f"列 {missing_columns} 不存在于CSV文件中", "success": False}
        
        if hue_column and hue_column not in df.columns:
            return {"error": f"分组列 '{hue_column}' 不存在于CSV文件中", "success": False}
        
        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)
        
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 获取文件名用于命名
        file_name = os.path.splitext(os.path.basename(csv_path))[0]
        save_path = os.path.join(save_dir, f'{file_name}_pairplot.png')
        
        # 创建配对图
        plt.figure(figsize=(12, 10))
        
        # 使用seaborn创建配对图
        pair_plot = sns.pairplot(
            df[numeric_columns + ([hue_column] if hue_column else [])],
            hue=hue_column,
            diag_kind='hist',
            plot_kws={'alpha': 0.6},
            diag_kws={'alpha': 0.7}
        )
        
        # 添加标题
        pair_plot.fig.suptitle('数值变量配对图', y=1.02)
        
        # 保存图表
        plt.tight_layout()
        pair_plot.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            "success": True,
            "plot_path": save_path,
            "columns_analyzed": numeric_columns,
            "hue_column": hue_column
        }
        
    except Exception as e:
        return {"error": str(e), "success": False}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        result = generate_scatter_plot_advanced(sys.argv[1], sys.argv[2], sys.argv[3])
        print(result)
    else:
        print("用法: python 散点图.py <csv文件路径> <x列名> <y列名> [hue列名] [style列名]")