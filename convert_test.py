import re


def capitalize_authors(line):
    # 使用正则表达式匹配作者名称
    author_pattern = r'((?:[A-Za-z]+(?:\s+[A-Za-z]+)*)(?:,\s*)?)+'

    # 将匹配到的作者名转换为以首字母大写的格式
    def replace_author(match):
        authors = match.group(0).strip().split(', ')
        # 处理每个作者的名字和姓氏
        capitalized_authors = [' '.join(part.capitalize() for part in author.strip().split()) for author in authors]

        # 返回处理后的作者名
        return ', '.join(capitalized_authors)

    return re.sub(author_pattern, replace_author, line)


def process_bbl_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified_lines = []

    for line in lines:
        # 检查是否是 \bibitem 开头的行
        if line.startswith(r'\bibitem'):
            modified_lines.append(line)  # 写入 \bibitem 行
            author_processed = False  # 每次新建 \bibitem 时重置标志
        elif not line.startswith(r'\newblock') and 'author_processed' in locals() and not author_processed:
            # 处理第一次遇到的作者行
            modified_line = capitalize_authors(line)
            modified_lines.append(modified_line)
            author_processed = True  # 设置标志，表示已经处理过
        else:
            # 直接写入其他行
            modified_lines.append(line)

            # 对整个文本执行正则化，替换 "Et~Al." 为 "et~al."
    final_output = ''.join(modified_lines).replace("Et~Al.", "et~al.")

    # 移除 DOI 和 URL 行
    final_output_lines = final_output.splitlines()
    cleaned_output = []

    for i, line in enumerate(final_output_lines):
        # 检查是否为 DOI 或 URL 行
        if re.search(r'DOI:', line) or re.search(r'\\url{', line):
            continue  # 跳过该行
        cleaned_output.append(line)

        # 替换 [J/OL] 为 [J]
    # 替换 [X/OL] 为 [X]
        # 替换 [X/OL] 或 [X/OLI] 为 [X] 并只保留前一个字母
    cleaned_output = [
        re.sub(r'\[([A-Z])/(OL|Ol)\]', r'[\1]', line) for line in cleaned_output
    ]
    cleaned_output = [line.replace('//', '') for line in cleaned_output]
    # 添加点符号到 [X] 后面（如果没有的话）
    cleaned_output = [
        re.sub(r'(\[[A-Z]\])(?!\.)', r'\1.', line) for line in cleaned_output
    ]

    # 将处理后的内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_output))

    # 输入您的 .bbl 文件路径和输出文件路径

input_bbl_file = 'old.bbl'  # 替换为您的 .bbl 文件名
output_bbl_file = 'new.bbl'  # 替换为您希望保存的文件名

process_bbl_file(input_bbl_file, output_bbl_file)