import os
import sys

from utils import (
    get_date_taken,
    is_screenshot,
    get_file_type,
    file_hash,
    copy_file
)

# Получаем исходную и целевую папки из аргументов командной строки
# Get source and target directories from command-line arguments
SOURCE = sys.argv[1]
TARGET = sys.argv[2]


def process():
    """
    Рекурсивно обходим все папки SOURCE и сортируем файлы по дате,
    убираем дубликаты по хешу, оставляя файл в более ранней папке
    Recursively walk through all folders in SOURCE and organize files by date,
    remove duplicates by hash, keeping the file in the earliest folder
    """
    seen_hashes = {}  # словарь: хеш → путь к уже скопированному файлу / hash → path

    for root, dirs, files in os.walk(SOURCE):
        for file in files:
            path = os.path.join(root, file)

            file_type = get_file_type(file)
            if not file_type:
                continue # skip unsupported files

            date = get_date_taken(path)
            year = str(date.year)
            month = f"{date.month:02}"

            # determine subfolder
            if file_type == "photo" and is_screenshot(file):
                subfolder = "screenshots"
            else:
                subfolder = file_type
                
            target_folder = os.path.join(TARGET, year, month, subfolder)
            os.makedirs(target_folder, exist_ok=True)

            destination = os.path.join(target_folder, file)
            h = file_hash(path)

            if h in seen_hashes:
                # Файл с таким же содержимым уже есть
                existing_path, existing_date = seen_hashes[h]
                # Оставляем файл в более ранней папке
                if date < existing_date:
                    # Новый файл старше → заменяем старый
                    os.remove(existing_path)
                    copy_file(path, destination)
                    seen_hashes[h] = (destination, date)
                    print(f"🔄 {file} (старее) заменил дубликат → {target_folder}")
                else:
                    print(f"❌ {file} дубликат, пропущен")
                continue
            else:
                copy_file(path, destination)
                seen_hashes[h] = (destination, date)
                print(f"✔ {file} → {target_folder}")


if __name__ == "__main__":
    process()
