import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np
from mcp.server.fastmcp import FastMCP

# 导入所有图表函数
from function.单变量 import generate_single_column_plots
from function.多变量相关性 import generate_scatter_plot
from function.类别型变量 import analyze_categorical_column
from function.热力图 import generate_correlation_heatmap
from function.散点图 import plot_csv_scatter
from function.数值型and类别型 import analyze_numeric_vs_categorical
from function.折线图 import plot_csv_column
from function.双轴折线图 import plot_dual_axis_line_chart
from function.qq图 import generate_qq_plot_with_test

# 创建MCP服务器
mcp = FastMCP("Chart Analysis Server")

@mcp.tool()
async def analyze_single_variable(
    csv_path: str, 
    y_column: str, 
    save_dir: str = r"D:\桌面"
) -> str:
    """
    从CSV文件中读取指定列数据，并生成四种统计图表(绘制直方图,绘制核密度估计图,绘制箱线图,绘制小提琴图)保存到指定目录
    
    参数:
        csv_path: CSV文件路径
        y_column: 需要分析的数值列名
        save_dir: 图片保存目录，默认为D:\桌面
    
    返回值:
        str: 操作结果的字符串描述
    """
    try:
        result = generate_single_column_plots(
            csv_path=csv_path,
            y_column=y_column,
            save_dir=save_dir
        )
        return f"输出成果：{result}"
    except Exception as e:
        return f"操作失败：{str(e)}"

@mcp.tool()
async def analyze_correlation(
    csv_path: str,
    x_column: str,
    y_column: str,
    save_dir: str = "./charts"
) -> Dict[str, Any]:
    """分析两个数值变量之间的相关性
    从CSV文件中读取指定列数据并绘制散点图
    
    参数:
        csv_path: CSV文件路径
        y_column: 用作y轴的列名
        x_column: 用作x轴的列名(可选)，缺省时使用行索引
        save_path: 图片保存路径，默认为'D:\\桌面'
    
    返回:
        操作结果状态字符串

    """
    try:
        result = generate_scatter_plot(
            csv_path=csv_path,
            x_column=x_column,
            y_column=y_column,
            save_dir=save_dir
        )
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def analyze_categorical(
    csv_path: str,
    y_column: str,
    save_dir: str = r"D:\桌面",
    top_n: int = None,
    min_freq: int = 1
) -> str:
    """分析类别型变量的分布特征
        对分类变量生成条形图、饼图和频数表
    
    参数:
        csv_path: CSV文件路径
        y_column: 要分析的分类型列名
        save_dir: 图片保存目录，默认为D:\桌面
        top_n: 仅显示频率最高的前n个类别（可选）
        min_freq: 显示最小频数阈值（可选）
    
    返回值:
        dict: 包含以下键的字典:
            - 'barplot_path': 条形图路径
            - 'piechart_path': 饼图路径
            - 'frequency_table': 频数表文本
            - 'summary_stats': 统计摘要
    """
    try:
        result = analyze_categorical_column(
            csv_path=csv_path,
            y_column=y_column,
            save_dir=save_dir,
            top_n=top_n,
            min_freq=min_freq
        )
        result_str = f"条形图路径: {result['barplot_path']}\n"
        result_str += f"饼图路径: {result['piechart_path']}\n\n"
        result_str += "频率表:\n"
        result_str += f"{result['frequency_table']}\n\n"
        result_str += "统计摘要:\n"
        result_str += f"{result['summary_stats']}\n\n"
        result_str += f"操作状态: {'成功' if result['success'] else '失败'}"
        return result_str
    except Exception as e:
        return "输出失败"

@mcp.tool()
async def generate_heatmap(
    csv_path: str,
    numeric_columns: List[str],
    save_dir: str = r"D:\桌面",
    corr_method: str = 'pearson',
    cluster: bool = False,
    annot: bool = True,
    cmap: str = 'coolwarm',
    figsize: Optional[tuple] = None
) -> str:
    """生成数值变量之间的相关系数热力图
    生成数值变量之间的相关系数热力图
    
    参数:
        csv_path: CSV文件路径
        numeric_columns: 需要分析的数值列名列表
        save_dir: 图片保存目录，默认为D:\桌面
        corr_method: 相关系数类型，可选 'pearson'(默认)/'spearman'/'kendall'
        cluster: 是否使用聚类排序，默认为False
        annot: 是否显示相关系数值，默认为True
        cmap: 颜色图谱，默认为'coolwarm'
        figsize: 图形尺寸，自动根据列数调整(可选覆盖)
    
    返回值:
        热力图保存路径，相关系数矩阵文本，使用的相关系数方法

    """
    try:
        result = generate_correlation_heatmap(
            csv_path=csv_path,
            numeric_columns=numeric_columns,
            save_dir=save_dir,
            corr_method=corr_method,
            cluster=cluster,
            annot=annot,
            cmap=cmap,
            figsize=figsize
        )
        result_str = f"热力图保存路径: {result['heatmap_path']}\n\n"
        result_str += f"相关系数计算方法: {result['method_used']}\n\n"
        result_str += "相关系数矩阵:\n"
        result_str += f"{result['correlation_matrix']}\n\n"
        result_str += f"操作状态: {'成功' if result['success'] else '失败'}"
        return result_str
    except Exception as e:
        return "操作失败"

@mcp.tool()
async def create_scatter_plot(
    csv_path: str,
    y_column: str,
    x_column: Optional[str] = None,
    save_dir: str = "./charts"
) -> Dict[str, Any]:
    """创建散点图
        从CSV文件中读取指定列数据并绘制散点图
    
    参数:
        csv_path: CSV文件路径
        y_column: 用作y轴的列名
        x_column: 用作x轴的列名(可选)，缺省时使用行索引
        save_dir: 图片保存目录，默认为D:\桌面
    
    返回:
        操作结果状态字符串  
    """
    try:
        result = plot_csv_scatter(
            csv_path=csv_path,
            y_column=y_column,
            x_column=x_column,
            save_path=save_dir
        )
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def analyze_numeric_categorical(
    csv_path: str,
    numeric_col: str,
    category_col: str,
    plot_types: List[str] = ["boxplot", "violin", "density"],
    show_mean: bool = True,
    show_median: bool = False,
    save_dir: str = r"D:\桌面"
) -> Dict[str, Any]:
    """分析数值变量与类别变量的关系"""
    try:
        result = analyze_numeric_vs_categorical(
            csv_path=csv_path,
            numeric_col=numeric_col,
            category_col=category_col,
            plot_types=plot_types,
            show_mean=show_mean,
            show_median=show_median,
            save_dir=save_dir
        )
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_line_plot(
    csv_path: str,
    column_name: str,
    save_dir: str = "./charts"
) -> Dict[str, Any]:
    """创建折线图"""
    try:
        result = plot_csv_column(
            csv_path=csv_path,
            column_name=column_name,
            save_path=save_dir
        )
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@mcp.tool()
async def create_dual_axis_plot(
    csv_path: str,
    y1_column: str,
    y2_column: str,
    x_column: Optional[str] = None,
    scale_type: str = 'linear',
    save_dir: str = "./charts"
) -> str:
    """创建双轴折线图"""
    try:
        result = plot_dual_axis_line_chart(
            csv_path=csv_path,
            y1_column=y1_column,
            y2_column=y2_column,
            x_column=x_column,
            scale_type=scale_type,
            save_dir=save_dir
        )
        data = result
        result_str = f"图表保存路径: {data['plot_path']}\n\n"

        # 添加温度统计信息
        result_str += "温度统计数据:\n"
        temp_stats = data['data_stats']['temperature']
        result_str += f"  平均值: {float(temp_stats['mean'])}\n"
        result_str += f"  中位数: {float(temp_stats['median'])}\n"
        result_str += f"  最小值: {float(temp_stats['min'])}\n"
        result_str += f"  最大值: {float(temp_stats['max'])}\n\n"

        # 添加销售额统计信息
        result_str += "销售额统计数据:\n"
        sales_stats = data['data_stats']['sales']
        result_str += f"  平均值: {float(sales_stats['mean'])}\n"
        result_str += f"  中位数: {float(sales_stats['median'])}\n"
        result_str += f"  最小值: {int(sales_stats['min'])}\n"
        result_str += f"  最大值: {int(sales_stats['max'])}\n\n"

        # 添加操作状态和警告信息
        result_str += f"操作状态: {'成功' if data['success'] else '失败'}\n"
        result_str += f"提示信息: {data['warning']}" 
        return result_str       
    except Exception as e:
        return "操作失败"

@mcp.tool()
async def create_qq_plot(
    csv_path: str,
    y_column: str,
    alpha: float = 0.05,
    save_dir: str = "./charts"
) -> Dict[str, Any]:
    """创建QQ图并进行正态性检验"""
    try:
        result = generate_qq_plot_with_test(
            csv_path=csv_path,
            y_column=y_column,
            alpha=alpha,
            save_dir=save_dir
        )
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run(transport='stdio')