import os

# 获取文件夹中的所有文件名
folder_path = 'Java'
file_names = os.listdir(folder_path)

# 去除文件名中的空格
for file_name in file_names:
    if ' ' in file_name:
        new_file_name = file_name.replace(' ', '')
        os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))

        # 更新md文件中的引用
        md_file_path = folder_path+'.md'
        with open(md_file_path, 'r') as file:
            file_content = file.read()
            file_content = file_content.replace(file_name, new_file_name)

        with open(md_file_path, 'w') as file:
            file.write(file_content)
