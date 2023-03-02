import os
import re

def extract_text(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search('\(\(\((.*)\)\)\)', content, re.DOTALL)
                if match:
                    extracted_text = match.group(1)
                    output_path = os.path.join(output_dir, filename)
                    with open(filename, 'w',encoding='utf-8') as out:
                        out.write(extracted_text)


def clear_comma_spaces(content):
    return re.sub(r',\s+', ',', content)

def clear_folder(folder_path):
    # 搜索文件夹下的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # 读取文件内容
            with open(file_path, 'r',encoding='utf-8') as f:
                content = f.read()
            # 清除逗号旁边的空格
            new_content = clear_comma_spaces(content)
            # 将修改后的内容写回文件
            with open(file_path, 'w',encoding='utf-8') as f:
                f.write(new_content)


def extract_text2(input_dir, file_path):
    # 搜索文件夹下的所有文件
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            print()
            file_path = os.path.join(root, file)
            # 读取文件内容
            with open(file_path, 'r',encoding='utf-8') as f:
                content = f.read()

            # 匹配最长的(( 和 ))之间的内容
            match = re.findall(r'\(\((.*?)\)\)', content, re.S)
            if match:
                longest_match = max(match, key=len)
                new_content = '(' + longest_match + ')'

                # 将新内容写入文件中
                with open(file, 'w',encoding='utf-8') as f:
                    f.write(new_content)
def extract_contents(content):
    regex = r'MultiPolygon.*\n'
    matches = re.findall(regex, content, re.DOTALL)
    result = []
    for match in matches:
        # 匹配(((和)))之间的内容
        regex = r'\(\(\((.*?)\)\)\)'
        matches = re.findall(regex, match, re.DOTALL)

        # 按照((分割内容，保留长度最大的子串
        max_substrs = []
        for match in matches:
            substrs = match.split('((')
            max_substr = max(substrs, key=len)
            max_substrs.append(max_substr)
        result.append(max_substr)
    return '\n'.join(result)

def extract_folder(folder_path):

    # 搜索文件夹下的所有文件
    for root, dirs, files in os.walk(folder_path):

        for file in files:
            results = []
            file_path = os.path.join(root, file)
            # 读取文件内容
            with open(file_path, 'r',encoding='utf-8') as f:
                content = f.read()
            # 提取内容并保留((和))包裹的最长内容
            extracted_content = extract_contents(content)
            # 将提取的内容添加到结果中
            results.append((file, extracted_content))
            with open(file, 'w', encoding='utf-8') as f:
                f.write(extracted_content)

if __name__ == '__main__':

    input_dir = r'C:\Users\Administrator\Desktop\hha'
    output_dir = r'C:\Users\Administrator\Desktop\lalo2'

    extract_folder(input_dir)
    # clear_folder(r"C:\Users\Administrator\Desktop\lalo\lola2")