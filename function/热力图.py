import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from typing import List, Optional, Tuple, Dict, Any

def generate_correlation_heatmap(
    csv_path: str,
    numeric_columns: List[str],
    save_dir: str = "./charts",
    corr_method: str = 'pearson',
    cluster: bool = False,
    annot: bool = True,
    cmap: str = 'coolwarm',
    figsize: Optional[Tuple[int, int]] = None
) -> Dict[str, Any]:
    """
    生成数值变量之间的相关系数热力图

    参数:
        csv_path: CSV文件路径
        numeric_columns: 需要分析的数值列名列表
        save_dir: 图片保存目录，默认为'./charts'
        corr_method: 相关系数类型，可选'pearson'/'spearman'/'kendall'
        cluster: 是否使用聚类排序，默认为False
        annot: 是否显示相关系数值，默认为True
        cmap: 颜色图谱，默认为'coolwarm'
        figsize: 图形尺寸，自动根据列数调整

    返回:
        包含热力图路径和相关系数矩阵的字典
    """
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_path)
        
        # 检查列是否存在
        missing_cols = [col for col in numeric_columns if col not in df.columns]
        if missing_cols:
            return {"error": f"列 {missing_cols} 不存在于CSV文件中", "success": False}
        
        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)
        
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 选择数值列
        numeric_df = df[numeric_columns].select_dtypes(include=[np.number])
        
        if numeric_df.empty:
            return {"error": "没有找到数值型列", "success": False}
        
        # 计算相关系数矩阵
        if corr_method == 'pearson':
            corr_matrix = numeric_df.corr(method='pearson')
            method_used = 'Pearson'
        elif corr_method == 'spearman':
            corr_matrix = numeric_df.corr(method='spearman')
            method_used = 'Spearman'
        elif corr_method == 'kendall':
            corr_matrix = numeric_df.corr(method='kendall')
            method_used = 'Kendall'
        else:
            return {"error": f"不支持的相关系数方法: {corr_method}", "success": False}
        
        # 设置图形尺寸
        if figsize is None:
            n_cols = len(numeric_columns)
            figsize = (max(8, n_cols * 1.2), max(8, n_cols * 1.2))
        
        # 创建热力图
        plt.figure(figsize=figsize)
        
        # 如果启用聚类，使用聚类排序
        if cluster:
            sns.clustermap(corr_matrix, annot=annot, cmap=cmap, 
                          fmt='.2f', figsize=figsize)
            save_path = os.path.join(save_dir, 
                                   f'{os.path.splitext(os.path.basename(csv_path))[0]}_correlation_cluster.png')
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            sns.heatmap(corr_matrix, annot=annot, cmap=cmap, fmt='.2f',
                       square=True, cbar_kws={'shrink': 0.8})
            plt.title(f'变量间相关系数热力图 ({method_used})')
            
            save_path = os.path.join(save_dir, 
                                   f'{os.path.splitext(os.path.basename(csv_path))[0]}_correlation_heatmap.png')
            plt.tight_layout()
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
        
        # 创建相关系数矩阵的字符串表示
        corr_str = corr_matrix.round(3).to_string()
        
        return {
            "success": True,
            "heatmap_path": save_path,
            "correlation_matrix": corr_str,
            "method_used": method_used,
            "num_variables": len(numeric_columns)
        }
        
    except Exception as e:
        return {"error": str(e), "success": False}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        cols = sys.argv[2:]
        result = generate_correlation_heatmap(sys.argv[1], cols)
        print(result)
    else:
        print("用法: python 热力图.py <csv文件路径> <列名1> <列名2> ...")