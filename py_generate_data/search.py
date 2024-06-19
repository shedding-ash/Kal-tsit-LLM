from functools import cache
import os

#@cache
def find_txt_files_with_prefixes(directory, prefixes):
    """
    递归查找指定目录下的所有txt文件，并检查每行是否以列表中的任一前缀开头。
    
    :param directory: 要搜索的目录路径。
    :param prefixes: 要检查的行前缀列表。
    :return: 一个包含所有符合条件的文件完整路径的列表。
    """
    matching_files = []  # 存储匹配的文件完整路径
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    flag = 0
                    for line in f:
                        for prefix in prefixes:
                            if line.strip().startswith(prefix):
                                flag =1
                                matching_files.append(filepath)
                                break  
                        if flag:
                            break
    return matching_files

# 使用示例
directory_path = 'D:\\github\\arknights\\result'  # 目录路径
prefixes = ['凯尔希:']  # 前缀列表
matching_files = find_txt_files_with_prefixes(directory_path, prefixes)
#print(matching_files)

# 写入文件
file_path = 'D:\\github\\arknights\\result\\obj_list.txt'
# 打开文件，准备写入
with open(file_path, 'w', encoding='utf-8') as file:
    # 遍历列表，将每个字符串写入文件的一行
    for item in matching_files:
        file.write(item + '\n')  

# # 读出为列表
# file_path = 'D:\\github\\arknights\\result\\obj_list.txt'
# # 初始化一个空列表来存储读取的字符串
# read_string_list = []
# with open(file_path, 'r', encoding='utf-8') as file:
#     for line in file:
#         # 移除每行末尾的换行符并添加到列表
#         read_string_list.append(line.strip())
      