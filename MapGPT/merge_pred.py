import os
import json

# 定义输入目录和输出文件路径
input_dir = 'datasets/exprs_map/4o/test/preds'
output_file = 'merged_preds.json'

# 初始化一个空列表来存储所有 JSON 数据
merged_data = []

# 遍历输入目录下的所有文件
for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            try:
                # 读取 JSON 文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    merged_data.append(data)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

# 将合并后的数据写入输出文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, indent=4, ensure_ascii=False)

if len(merged_data) == 216:
    print(f"All JSON files merged into {output_file}")
