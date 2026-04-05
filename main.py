import os
import sys
import shutil
import hashlib
from datetime import datetime
from PIL import Image

# Получаем исходную и целевую папки из аргументов командной строки
# Get source and target directories from command-line arguments
SOURCE = sys.argv[1]
TARGET = sys.argv[2]

PHOTO_EXT = (".jpg", ".jpeg", ".png", ".heic")
VIDEO_EXT = (".mp4", ".mov", ".avi", ".mkv")


def get_date_taken(path):
    """
    Получаем дату создания фото из EXIF или fallback на дату файла
    Get photo creation date from EXIF or fallback to file modification date
    """
    try:
        img = Image.open(path)
        exif = img.getexif()
        if exif:
            date = exif.get(36867)
            if date:
                return datetime.strptime(date, "%Y:%m:%d %H:%M:%S")
    except:
        pass
    timestamp = os.path.getmtime(path)
    return datetime.fromtimestamp(timestamp)


def is_screenshot(filename):
    """
    Проверяем, является ли файл скриншотом
    Check if the file is a screenshot
    Поддерживает английские и русские названия
    Supports English and Russian names
    """
    name = filename.lower()
    # английские и русские варианты
    return any(keyword in name for keyword in ["screenshot", "screen", "снимок экрана"])


def get_file_type(file):
    """
    Определяем тип файла: фото или видео
    Determine file type: photo or video
    """
    ext = file.lower()
    if ext.endswith(PHOTO_EXT):
        return "photo"
    elif ext.endswith(VIDEO_EXT):
        return "video"
    return None


def file_hash(path, chunk_size=8192):
    """
    Вычисляем md5 хеш файла для идентификации дубликатов
    Calculate md5 hash of a file to identify duplicates
    """
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def copy_file(src, dst):
    """
    Копируем файл, если его ещё нет в целевой папке
    Copy file if it does not already exist in the destination
    """
    if not os.path.exists(dst):
        shutil.copy2(src, dst)


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
                continue

            date = get_date_taken(path)
            year = str(date.year)
            month = f"{date.month:02}"

            subfolder = "screenshots" if is_screenshot(file) else file_type
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