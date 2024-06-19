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
                merged.append(f"[{current_speaker}] {' '.join(current_dialog)}")
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
                        merged.append(f"[{current_speaker}] {' '.join(current_dialog)}")
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
                        merged.append(f"[{current_speaker}] {' '.join(current_dialog)}")
                    current_speaker = speaker
                    current_dialog = [line]
    
    # 处理最后累积的对话
    if current_dialog:
        merged.append(f"[{current_speaker}] {' '.join(current_dialog)}")
    
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

    SAVE_PATH = 'D:\\github\\arknights\\result\\test\\'

    # 主线
    x = r'D:\github\arknights\result\obj.txt'
    x1 = 'D:\\github\\arknights\\result\\'
    filter_and_save(x, "_filtered", x1)

