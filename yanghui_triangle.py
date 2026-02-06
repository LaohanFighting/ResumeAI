# -*- coding: utf-8 -*-
"""
杨辉三角（帕斯卡三角）生成器
"""

def generate_pascal_triangle(n):
    """
    生成杨辉三角（帕斯卡三角）
    
    参数:
        n: 要生成的行数
    
    返回:
        二维列表，表示杨辉三角
    """
    triangle = []
    
    for i in range(n):
        # 每一行的第一个元素总是1
        row = [1]
        
        # 计算中间的元素（除了第一行和第二行）
        if i > 0:
            prev_row = triangle[i - 1]
            for j in range(len(prev_row) - 1):
                # 每个元素等于上一行相邻两个元素之和
                row.append(prev_row[j] + prev_row[j + 1])
            # 每一行的最后一个元素也是1
            row.append(1)
        
        triangle.append(row)
    
    return triangle


def print_pascal_triangle(triangle):
    """
    打印杨辉三角，居中对齐
    
    参数:
        triangle: 二维列表，表示杨辉三角
    """
    n = len(triangle)
    # 计算最后一行需要的宽度（用于居中对齐）
    max_width = len(' '.join(map(str, triangle[-1])))
    
    for row in triangle:
        # 将每行转换为字符串
        row_str = ' '.join(map(str, row))
        # 居中对齐打印
        print(row_str.center(max_width))


def print_pascal_triangle_formatted(triangle):
    """
    打印杨辉三角，格式化输出（每个数字占固定宽度）
    
    参数:
        triangle: 二维列表，表示杨辉三角
    """
    n = len(triangle)
    # 计算最大数字的位数
    max_num = max(max(row) for row in triangle)
    width = len(str(max_num)) + 1
    
    for i, row in enumerate(triangle):
        # 计算每行前面的空格数（用于居中对齐）
        spaces = ' ' * (width * (n - i - 1) // 2)
        # 格式化每行的数字
        row_str = ''.join(f'{num:>{width}}' for num in row)
        print(spaces + row_str)


if __name__ == "__main__":
    import sys
    import io
    # 设置标准输出为 UTF-8 编码
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    # 生成10行的杨辉三角
    n = 10
    print(f"杨辉三角（{n}行）：\n")
    
    triangle = generate_pascal_triangle(n)
    
    # 方法1：简单打印
    print("方法1 - 简单打印：")
    print_pascal_triangle(triangle)
    
    print("\n" + "="*50 + "\n")
    
    # 方法2：格式化打印
    print("方法2 - 格式化打印：")
    print_pascal_triangle_formatted(triangle)
    
    print("\n" + "="*50 + "\n")
    
    # 方法3：直接打印列表形式
    print("方法3 - 列表形式：")
    for i, row in enumerate(triangle):
        print(f"第{i+1}行: {row}")
