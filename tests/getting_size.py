import os

"""
Это учебный скрипт чтобы понять правильно ли определяется размер файла, лежащего по указанному пути
"""

file_path = "C:/projects_c/test_scenario/downloads/sbisplugin-setup-web.exe"

if os.path.exists(file_path):
    file_size = os.path.getsize(file_path)
    print(f"Размер файла: {file_size} байт ({file_size / (1024 * 1024):.2f} МБ)")
else:
    print("Файл не найден")