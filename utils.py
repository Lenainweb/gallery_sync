import os
import shutil
import hashlib
from datetime import datetime
from PIL import Image

from config import PHOTO_EXT, VIDEO_EXT


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
