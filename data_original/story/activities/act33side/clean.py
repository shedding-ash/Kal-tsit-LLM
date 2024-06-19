import re
import os
import glob
import yaml

# 定义一个函数来处理每一行，检查是否包含指定的标签
def should_keep_line(line):
    # 检查是否包含特定的标签
    if re.search(r'\[name=".*?"\]|\[dialog\]|\[Dialog\]|\[Subtitle', line):
        return True
    # 检查是否是中文的一句话
    if re.match(r'^[\u4e00-\u9fa5\uFF0C\u3002\uFF1F\uFF01\u3001\u2014\u2026\s]+$', line):
        return True
    # 检查并提取subtitle的内容
    match = re.match(r'\[Subtitle\(text="(.*?)".*?\)\]', line)
    if match:     
        return match.group(1)
    return False


def filter_and_save(file_path, suffix='filtered', save_path=None):
    # 构建完整的文件路径
    #full_file_path = os.path.join(file_path, file_name)

    # 如果没有指定保存路径，则默认为当前目录
    if save_path is None:
        save_path = '.'

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    filtered_lines = [line for line in lines if should_keep_line(line)]

    # # 创建新文件名，添加后缀
    # base_name = os.path.splitext(file_name)[0]
    # new_file_name = f"{base_name}{suffix}.txt"

    # 使用 os.path.basename() 获取路径中文件名的部分
    file_name = os.path.basename(file_path)
    # 使用 os.path.splitext() 分离文件名和扩展名
    base_name, extension = os.path.splitext(file_name)
    new_file_name = f"{base_name}{suffix}{extension}"

    # 如果save_path不是当前目录，添加到文件名中
    if save_path != '.':
        new_file_name = os.path.join(save_path, new_file_name)

    # 将过滤后的内容写入新文件
    with open(new_file_name, 'w', encoding='utf-8') as file:
        for line in filtered_lines:
            file.write(line)

    print(f"处理完成，新文件已创建：{new_file_name}")

# 示例使用：
# filter_and_save('example.txt', '/path/to/directory')


if __name__ == "__main__":
    
    folder = ["act33side", "act18d0", "act18d3", "act17side"]
    map_yaml_path = "D:\\github\\arknights\\result\\命名映射.yaml"

    with open(map_yaml_path, "r", encoding="utf-8") as f:
        map_yaml = yaml.safe_load(f)

    # 遍历文件夹列表
    for item in folder:
        # 文件夹路径
        base_path = 'D:\\github\\arknights\\story\\activities\\'
        base_path += item  # 将文件夹名称添加到基本路径
        
        # 首先检查item是否在主活动字典中
        if item in map_yaml["activity"]:
            chinese_name = map_yaml["activity"][item]
        # 否则，检查是否在插曲字典中
        elif item in map_yaml["sidestory"]:
            chinese_name = map_yaml["sidestory"][item]
        # 如果找不到对应的映射
        else:
            chinese_name = "未知活动"  

        # 保存路径
        save_path = 'D:\\github\\arknights\\result\\'
        save_path += chinese_name  # 将中文名称添加到保存路径

        # 要匹配的文件模式，根据item动态构建模式
        file_pattern = os.path.join(base_path, f'level_{item}_*.txt')       
        # 使用glob模块找到所有匹配的文件
        for file_path in glob.glob(file_pattern):
            # 对每个文件调用filter_and_save函数
            filter_and_save(file_path, "filtered", save_path)