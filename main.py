# 脚本功能：遍历data目录下的所有文件（忽略-开头的文件），并根据输入的命令行参数输出手心输入法、搜狗输入法、百度输入法词库。支持多音字。
# 命令行参数：baidu、sougou、shouxin
# data目录下的文件编码为UTF-8，每一行一个词

import os
import argparse
from pypinyin import pinyin, Style

# 生成拼音
def convert_to_pinyin(text):
    pinyin_list = pinyin(text, style=Style.NORMAL, heteronym=False,errors="ignore")
    pinyin_str = "'".join([''.join(char) for char in pinyin_list])
    return pinyin_str

# 写入文件
def read_file_in_chunks(file_path, output_file_name, output_encoding, output_format, chunk_size=100):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            pinyin_line = convert_to_pinyin(line.strip())
            
            if output_format == 'baidu' or output_format == 'shouxin':
                new_line = f"{line.strip()}\t{pinyin_line}\t3"
            elif output_format == 'sougou':
                new_line = f"{pinyin_line}\t{line.strip()}"
            
            with open(output_file_name, "a", encoding=output_encoding) as output_file:
                output_file.write(new_line + '\n')

# 添加命令行参数
parser = argparse.ArgumentParser(description='请输入你要生成的词库类型，sougou、baidu、shouxin')
parser.add_argument('output_format', choices=['baidu', 'shouxin', 'sougou'], help='Choose the output format')
args = parser.parse_args()

# 根据命令行参数选择输出文件名、编码格式和格式
if args.output_format == 'baidu':
    output_file_name = 'Zakary百度词库.txt'
    output_encoding = 'utf-16'
    output_format = 'baidu'
elif args.output_format == 'shouxin':
    output_file_name = 'Zakary手心词库.txt'
    output_encoding = 'utf-16'
    output_format = 'shouxin'
elif args.output_format == 'sougou':
    output_file_name = 'Zakary搜狗词库.txt'
    output_encoding = 'cp936'
    output_format = 'sougou'

# 获取当前脚本所在目录的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, 'data')

# 遍历data目录下的所有文件
for file_name in os.listdir(data_dir):
    file_path = os.path.join(data_dir, file_name)
    if os.path.isfile(file_path) and file_name[0] != "-":
        read_file_in_chunks(file_path, output_file_name, output_encoding, output_format)