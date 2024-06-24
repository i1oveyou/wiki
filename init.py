import os
import subprocess
cnt=0

def find_and_convert(directory):
    global cnt
    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'index.md':
                # 获取 markdown 文件的完整路径
                markdown_file = os.path.join(root, file)
                # 生成对应的 html 文件路径
                html_file = os.path.join(root, 'index.html')
                # 构建 pandoc 命令
                command = f"pandoc --from markdown --to html -o {html_file} --template=bootstrap_menu.html --toc {markdown_file}"
                #print(f"Executing command: {command}")
                cnt=cnt+1
                print(str(cnt)+html_file)
                # 执行命令
                subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 指定需要遍历的目录
directory_to_search = './post'
find_and_convert(directory_to_search)
