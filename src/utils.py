import os
import shutil
import hashlib
from datetime import datetime

from PIL import Image
from pillow_heif import register_heif_opener


from config import PHOTO_EXT, VIDEO_EXT


""" 
Register HEIC support in Pillow
This allows Pillow to open and process HEIC/HEIF images.
Without this, attempting to open HEIC files with Image.open() will fail.
"""
register_heif_opener()

def get_date_taken(path):
    """
    Получаем дату создания фото из EXIF или fallback на дату файла
    Get photo creation date from EXIF or fallback to file modification date
    """
    try:
        img = Image.open(path)
        exif = img.getexif()
        if exif:
            date = exif.get(36867) # EXIF tag for DateTimeOriginal
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


def process_gallery(source, target, verbose=True):
    """
    Gallery sorting function

    - Sorts photos and videos by date
    - Separates screenshots
    - Removes duplicates using md5 hash

    source: source folder
    target: target folder
    verbose: print log messages
    """
    seen_hashes = {}  # hash -> (путь к файлу, дата)

    for root, dirs, files in os.walk(source):
        for file in files:
            path = os.path.join(root, file)

            file_type = get_file_type(file)
            if not file_type:
                continue  # skip unsupported files

            date = get_date_taken(path)
            year = str(date.year)
            month = f"{date.month:02}"

            # determine subfolder
            if file_type == "photo" and is_screenshot(file):
                subfolder = "screenshots"
            else:
                subfolder = file_type

            target_folder = os.path.join(target, year, month, subfolder)
            os.makedirs(target_folder, exist_ok=True)

            destination = os.path.join(target_folder, file)
            h = file_hash(path)

            if h in seen_hashes:
                existing_path, existing_date = seen_hashes[h]
                if date < existing_date:
                    # New file is older → replace the existing file
                    os.remove(existing_path)
                    copy_file(path, destination)
                    seen_hashes[h] = (destination, date)
                    if verbose:
                        print(f"🔄 {file} (старее) заменил дубликат → {target_folder}")
                else:
                    if verbose:
                        print(f"❌ {file} дубликат, пропущен")
                continue
            else:
                copy_file(path, destination)
                seen_hashes[h] = (destination, date)
                if verbose:
                    print(f"✔ {file} → {target_folder}")
