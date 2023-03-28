#1.train_val-DatasetSeqFeatureMappings.dataset的处理
#txt文件去除它的第1，4，7，10，13，16，19，22，25等行
from itertools import islice
import fileinput
with fileinput.input(files=('train_val-DatasetSeqFeatureMappings.dataset',), inplace=False) as f:
    with open('train-val.txt', 'w') as new_f:
        for line in f:
            if (f.filelineno() - 1) % 3 != 0:
                new_f.write(line)

import fileinput
with fileinput.input(files=('train-val.txt',), inplace=False) as f:
    with open('train-val1.txt', 'w') as new_f:
        for line in f:
            if (f.filelineno() % 2) != 0:
                line = line.strip()
                line = 'B' * 7 + line.strip() + 'B' * 7
            else:
                line = line.strip()
                line = '0' * 7 + line.strip() + '0' * 7
            new_f.write(line + '\n')

import csv
with open('train-val1.txt', 'r') as f:
    # 创建csv文件并写入表头
    with open('output.csv', 'w',newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['feature', 'label'])
        # 逐行读取文件
        lines = f.readlines()
        for i in range(0, len(lines), 2):
            # 获取序列和标签
            sequence = lines[i].strip()
            label = lines[i + 1].strip()
            # 使用滑动窗口切分序列
            for j in range(len(sequence) - 14):
                # sub_sequence = sequence[j:j + 11]
                sub_sequence = ' '.join(sequence[j:j + 15])
                # 获取标签
                sub_label = label[j + 7]
                # 写入csv文件
                writer.writerow([sub_sequence, sub_label])

#随机采样
import pandas as pd
# 读取文件
df = pd.read_csv('output.csv')
# 选取 label 为 0 的数据
df_0 = df[df['label'] == 0].sample(n=45690)
# 选取 label 为 1 的数据
df_1 = df[df['label'] == 1]
# 纵向合并两种数据
df_new = pd.concat([df_0, df_1], axis=0)
# 写入新文件
df_new.to_csv('strict.csv', index=False)

# 2.independent-DatasetSeqFeatureMappings.dataset的处理
# #txt文件去除它的第1，4，7，10，13，16，19，22，25等行
# from itertools import islice
# import fileinput
# with fileinput.input(files=('independent-DatasetSeqFeatureMappings.dataset',), inplace=False) as f:
#     with open('independent.txt', 'w') as new_f:
#         for line in f:
#             if (f.filelineno() - 1) % 3 != 0:
#                 new_f.write(line)

# import fileinput
# with fileinput.input(files=('independent.txt',), inplace=False) as f:
#     with open('train-val1.txt', 'w') as new_f:
#         for line in f:
#             if (f.filelineno() % 2) != 0:
#                 line = line.strip()
#                 line = 'B' * 7 + line.strip() + 'B' * 7
#             else:
#                 line = line.strip()
#                 line = '0' * 7 + line.strip() + '0' * 7
#             new_f.write(line + '\n')

# import csv
# with open('independent1.txt', 'r') as f:
#     # 创建csv文件并写入表头
#     with open('independent15.csv', 'w',newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerow(['feature', 'label'])
#         # 逐行读取文件
#         lines = f.readlines()
#         for i in range(0, len(lines), 2):
#             # 获取序列和标签
#             sequence = lines[i].strip()
#             label = lines[i + 1].strip()
#             # 使用滑动窗口切分序列
#             for j in range(len(sequence) - 14):
#                 # sub_sequence = sequence[j:j + 11]
#                 sub_sequence = ' '.join(sequence[j:j + 15])
#                 # 获取标签
#                 sub_label = label[j + 7]
#                 # 写入csv文件
#                 writer.writerow([sub_sequence, sub_label])

