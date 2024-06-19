import json

def save_as_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

def extract(list_data, target_name):
    input, output = [], []
    system_default = "你是凯尔希，罗德岛的医生，阿米娅与博士的同伴，作为罗德岛战略指挥系统的重要组成人员活跃在各项目中"
    system = system_default
    input_default = ""
    flag = 0
    # 检查是否有target_name的行
    for i, line in enumerate(list_data):
        if line.startswith(f"{target_name}:"):
            # 检查是否是第一行
            if i == 0:               
                flag = 1
                input.append(input_default)
            elif i == 1:
                flag = 1
                input.append(list_data[0])
            else:
                input.append(list_data[i - 1])
            output.append(line)
    if not flag:
        system = list_data[0]
    return system, input, output


def extract_dialogues(target_name, corpus_path):
    with open(corpus_path, "r", encoding="utf-8") as file:
        content = file.read()

    # 将内容按照[Dialog]分割成不同的对话部分
    parts = content.split("[Dialog]\n")
    parts_data = []
    # part是dialog分割的一个字符串列表，对话块
    for part in parts:
        part = part.split("\n")
        # 检查目标角色是否在对话中
        if any(target_name in line for line in part):
            it = []
            # extract函数获取这段对话块中的system input output，
            # 其中system是一个字符串，input和output是字符串列表
            system, input, output = extract(part,target_name)

            # 第一个字典需要有system
            if input:
                it.append({
                    "system": system,
                    "input": input[0],
                    "output": output[0]
                })
                # 插入后续数据
                for i in range(1, max(len(input), len(output))):
                    it.append({
                        "input": input[i],
                        "output": output[i]
                    })
                parts_data.append({"conversation": it})

    return parts_data

if __name__ == "__main__":
    target_name = "凯尔希"
    file_path = "D:\\github\\arknights\\result\\obj_list.txt"
    # file_path = r"D:\github\arknights\result\obj.txt"
    result = []
    # 读出为列表
    read_string_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # 移除每行末尾的换行符并添加到列表
            read_string_list.append(line.strip())
    for item in read_string_list:
        res = extract_dialogues(target_name, item)
        # print(res)
        result += res

    # 指定JSON文件的路径
    json_file_path = 'output.json'
    # 调用函数保存JSON
    save_as_json(result, json_file_path)

    