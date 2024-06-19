def extract(list_data, target_name):
    input, output = [], []
    system_default = '你是凯尔希，罗德岛的医生，阿米娅与博士的同伴，作为罗德岛战略指挥系统的重要组成人员活跃在各项目中'
    system = system_default
    input_default = ''
    flag = 0
    # 检查是否有target_name的行
    for i, line in enumerate(list_data):
        if line.startswith(f'{target_name}:'):
            # 检查是否是第一行
            if i == 0:               
                flag = 1
                input.append(input_default)
            if i == 1:
                flag = 1
                input.append(list_data[0])
            else:
                input.append(list_data[i - 1])
            output.append(line)
    if not flag:
        system = list_data[0]
    return system, input, output

# 示例使用
list_data = [
    "艾利奥特: ......为什么我们不去米诺斯？ 我不确定......我不确定比起那些雇佣兵，你到底可信到什么地步......你们有什么区别？",
    "凯尔希: 区别在于你还活着。",
    "艾利奥特: ......反正你已经有安排了吧，接下来要怎么做？",
    "凯尔希: 找到一个可信任的人，我们要靠黑市的手段离开伊巴特。",
    "艾利奥特: 然后去哪儿？莱塔尼亚？玻利瓦尔？",
    "凯尔希: ......在我回答之前，你必须清楚，任何选择都只是逃避的一种方案。 你无法生活，无处可去，无路可逃。 你是否做好了过去的生活早已支离破碎的觉悟？你是否真的有意识到这一点，而不是在各种突如其来的事件中失了神？",
    "艾利奥特: ......别总是这么高高在上......"
    # 省略其他对话
]

system, input, output = extract(list_data, '凯尔希')
print("System:", system)
print("Input:", input)
print("Output:", output)