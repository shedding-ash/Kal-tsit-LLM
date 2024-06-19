import re
import os
import glob
import yaml

# 定义一个函数来处理每一行，检查是否包含指定的标签
def should_keep_line(line):
    # 检查是否包含特定的标签
    if re.search(r'\[name=".*?"\]|\[Dialog\]', line):#|\[dialog\]
        return True
    # 检查并提取subtitle的内容
    match = re.match(r'\[Subtitle\(text="(.*?)".*?\)\]', line)
    if match:     
        return match.group(1)
    # 检查是否是中文的一句话
    if re.match(r'^[\u4e00-\u9fa5\uFF0C\u3002\uFF1F\uFF01\u3001\u2014\u2026\s]+$', line):
        return True   
    return False
# 合并相邻相同name的对话
def merge_dialogues(input_str):
    # 正则表达式匹配[name="..."]和[Dialog]
    dialog_pattern = re.compile(r'^\[Dialog\]$')
    name_pattern = re.compile(r'\[name="(.*?)"\]')
    
    # 初始化变量
    merged = []
    current_speaker = None
    current_dialog = []
    
    for line in input_str:
        # 检查是否是[Dialog]标签
        if dialog_pattern.match(line):
            if current_dialog:
                if not current_dialog[-1].endswith('\n'):
                    current_dialog[-1] += '\n'
                merged.append(f"{current_speaker}: {' '.join(current_dialog)}")
                current_dialog = []
            merged.append(line)  # 添加[Dialog]标签
        else:
            # 检查是否包含[name="..."]前缀
            match = name_pattern.match(line)
            if match:
                speaker = match.group(1)
                content = line[match.end():].strip()
                if speaker == current_speaker:  # 同一角色的连续对话
                    current_dialog.append(content)
                else:  # 角色改变，先保存之前的对话
                    if current_dialog:
                        if not current_dialog[-1].endswith('\n'):
                            current_dialog[-1] += '\n'
                        merged.append(f"{current_speaker}: {' '.join(current_dialog)}")
                    current_speaker = speaker
                    current_dialog = [content]
            else:# 无前缀描写
                speaker = None
                line = line.rstrip('\n')
                if speaker == current_speaker:
                    current_dialog.append(line)
                else:
                    if current_dialog:
                        if not current_dialog[-1].endswith('\n'):
                            current_dialog[-1] += '\n'
                        merged.append(f"{current_speaker}: {' '.join(current_dialog)}")
                    current_speaker = speaker
                    current_dialog = [line]
    
    # 处理最后累积的对话
    if current_dialog:
        current_dialog += '\n'
        merged.append(f"{current_speaker}: {' '.join(current_dialog)}")
    
    # 返回合并后的字符串
    return merged

def filter_and_save(file_path, suffix='_filtered', save_path1=None):
    # 构建完整的文件路径
    #full_file_path = os.path.join(file_path, file_name)

    # 如果没有指定保存路径，则默认为当前目录
    if save_path1 is None:
        save_path1 = '.'

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    filtered_lines = []
    for line in lines:
        result = should_keep_line(line)
        if result is True:
            filtered_lines.append(line)
        elif result is False:
            None
        else:  # 如果结果是非布尔值，添加返回的值
            filtered_lines.append(result + '\n')

    filtered_lines = merge_dialogues(filtered_lines)

    if filtered_lines:

        if filtered_lines[0] != ('[Dialog]\n' or '[dialog]\n'):
            filtered_lines.insert(0, '[Dialog]\n')  # 在列表开头插入【dialog】

        # 检查最后一个元素是否是【dialog】
        if filtered_lines[-1] != ('[Dialog]\n' or '[dialog]\n'):
            filtered_lines.append('[Dialog]\n')  # 在列表末尾添加【dialog】

    # 使用 os.path.basename() 获取路径中文件名的部分
    file_name = os.path.basename(file_path)
    # 使用 os.path.splitext() 分离文件名和扩展名
    base_name, extension = os.path.splitext(file_name)
    new_file_name = f"{base_name}{suffix}{extension}"

    # 如果save_path不是当前目录，添加到文件名中
    if save_path1 != '.':
        new_file_name = os.path.join(save_path1, new_file_name)

    # 如果save_path不存在，创建
    if not os.path.exists(save_path1):
        os.makedirs(save_path1)

    # 将过滤后的内容写入新文件
    with open(new_file_name, 'w', encoding='utf-8') as file:
        for line in filtered_lines:
            file.write(line)

    print(f"处理完成，新文件已创建：{new_file_name}")

# 示例使用：
# filter_and_save('example.txt', '/path/to/directory')


if __name__ == "__main__":
    
    # 故事集和活动
    folder1 = [
    "a001", "act3d0", "act5d0", "act9d0", "act11d0", "act12d0", "act12side",
    "act13d5", "act13side", "act14side", "act15d0", "act15side", "act16d5", "act16side",
    "act17d0", "act17side", "act18d0", "act18d3", "act18side", "act19side", "act20side",
    "act21side", "act22side", "act23side", "act24side", "act25side", "act26side", "act27side",
    "act28side", "act29side", "act30side", "act31side", "act32side", "act33side",
    "act4d0", "act6d5", "act7d5", "act7mini", "act8mini", "act9mini", "act10d5",
    "act10mini", "act11mini", "act12mini", "act13d0", "act13mini", "act14mini",
    "act15d5", "act15mini", "act16mini"
    ]

    map_yaml_path = "D:\\github\\arknights\\result\\命名映射.yaml"

    with open(map_yaml_path, "r", encoding="utf-8") as f:
        map_yaml = yaml.safe_load(f)
    
    SAVE_PATH = 'D:\\github\\arknights\\result\\'

    # 遍历文件夹列表
    for item in folder1:
        # 文件夹路径
        base_path = 'D:\\github\\arknights\\story\\activities\\'
        base_path += item  # 将文件夹名称添加到基本路径
        
        # 保存路径
        save_path1 = SAVE_PATH

        # 首先检查item是否在主活动字典中
        if item in map_yaml["activity"]:
            chinese_name = map_yaml["activity"][item]
            save_path1 += 'activity\\'

        # 否则，检查是否在插曲字典中
        elif item in map_yaml["sidestory"]:
            chinese_name = map_yaml["sidestory"][item]
            save_path1 += 'sidestory\\'
        # 如果找不到对应的映射
        else:
            chinese_name = "未知活动"
            save_path1 += 'unknown\\'  

        save_path1 += chinese_name  # 将中文名称添加到保存路径

        # 要匹配的文件模式，根据item动态构建模式
        file_pattern = os.path.join(base_path, f'level_{item}_*.txt')       
        # 使用glob模块找到所有匹配的文件
        for file_path in glob.glob(file_pattern):
            # 对每个文件调用filter_and_save函数
            filter_and_save(file_path, "_filtered", save_path1)

    # 主线
    base_path = 'D:\\github\\arknights\\story\\obt\\main\\'
    save_path2 = SAVE_PATH + 'main\\'
    # 要匹配的文件模式，根据item动态构建模式
    file_pattern = os.path.join(base_path, f'level_*.txt')       
    # 使用glob模块找到所有匹配的文件
    for file_path in glob.glob(file_pattern):
        # 对每个文件调用filter_and_save函数
        filter_and_save(file_path, "_filtered", save_path2)

    # 干员秘录
    base_path = 'D:\\github\\arknights\\story\\obt\\memory\\'
    save_path3 = SAVE_PATH + 'memory\\'
    # 要匹配的文件模式，根据item动态构建模式
    file_pattern = os.path.join(base_path, f'story_*.txt')       
    # 使用glob模块找到所有匹配的文件
    for file_path in glob.glob(file_pattern):
        # 对每个文件调用filter_and_save函数
        filter_and_save(file_path, "_filtered", save_path3)