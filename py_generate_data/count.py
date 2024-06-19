import json
with open('output.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
print(len(data))