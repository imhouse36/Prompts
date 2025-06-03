#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件后缀名批量修改工具
将目录下的.mdc和.txt文件后缀改为.md
"""

import os
import sys
from pathlib import Path

def rename_files_to_md(directory_path):
    """
    将指定目录下的.mdc和.txt文件后缀改为.md
    
    Args:
        directory_path (str): 目标目录路径
    
    Returns:
        dict: 包含成功和失败统计的字典
    """
    if not os.path.exists(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在")
        return {'success': 0, 'failed': 0, 'errors': ['目录不存在']}
    
    success_count = 0
    failed_count = 0
    errors = []
    
    # 支持的源文件后缀
    source_extensions = ['.mdc', '.txt']
    
    try:
        # 遍历目录及其子目录
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_name, file_ext = os.path.splitext(file)
                
                # 检查是否为目标后缀
                if file_ext.lower() in source_extensions:
                    new_file_path = os.path.join(root, file_name + '.md')
                    
                    try:
                        # 检查目标文件是否已存在
                        if os.path.exists(new_file_path):
                            print(f"警告：目标文件已存在，跳过 {file_path}")
                            continue
                        
                        # 重命名文件
                        os.rename(file_path, new_file_path)
                        print(f"成功：{file_path} -> {new_file_path}")
                        success_count += 1
                        
                    except Exception as e:
                        error_msg = f"重命名失败 {file_path}: {str(e)}"
                        print(f"错误：{error_msg}")
                        errors.append(error_msg)
                        failed_count += 1
    
    except Exception as e:
        error_msg = f"遍历目录时出错: {str(e)}"
        print(f"错误：{error_msg}")
        errors.append(error_msg)
    
    return {
        'success': success_count,
        'failed': failed_count,
        'errors': errors
    }

def main():
    """
    主函数：处理命令行参数并执行文件重命名
    """
    # 获取命令行参数中的目录路径，如果没有则使用当前目录
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
    else:
        target_directory = input("请输入目标目录路径（回车使用当前目录）: ").strip()
        if not target_directory:
            target_directory = os.getcwd()
    
    print(f"开始处理目录: {target_directory}")
    print("正在查找 .mdc 和 .txt 文件...")
    
    # 执行重命名操作
    result = rename_files_to_md(target_directory)
    
    # 输出结果统计
    print("\n=== 操作完成 ===")
    print(f"成功重命名: {result['success']} 个文件")
    print(f"失败: {result['failed']} 个文件")
    
    if result['errors']:
        print("\n错误详情:")
        for error in result['errors']:
            print(f"  - {error}")
    
    if result['success'] > 0:
        print("\n所有符合条件的文件已成功重命名为 .md 后缀")
    else:
        print("\n未找到需要重命名的文件")

if __name__ == "__main__":
    main()