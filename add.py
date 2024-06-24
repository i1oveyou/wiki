import os
import subprocess

def get_modified_index_files():
    
    command="git add ."
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 获取git status或diff中所有修改过的index.md文件
    result = subprocess.run(['git', 'diff', '--name-only', 'HEAD'], capture_output=True, text=True)
    modified_files = result.stdout.splitlines()
    index_files = [file for file in modified_files if file.endswith('index.md')]
    return index_files

def process_markdown_file(markdown_file):
    # 获取文件所在的目录路径
    root = os.path.dirname(markdown_file)
    # 生成对应的 html 文件路径
    html_file = os.path.join(root, 'index.html')

    # 构建 pandoc 命令
    command = f"pandoc --from markdown --to html -o {html_file} --template=bootstrap_menu.html --toc {markdown_file}"
    print(f"Executing command: {command}")

    # 执行命令，忽略输出报错
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    # 获取所有修改过的 index.md 文件
    modified_index_files = get_modified_index_files()
    
    for markdown_file in modified_index_files:
        process_markdown_file(markdown_file)

if __name__ == '__main__':
    main()