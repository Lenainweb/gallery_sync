# gallery_sync  
Organize your photos and videos by date, handle screenshots, and remove duplicates.

---

## Особенности / Features

- Photo support: `.jpg`, `.jpeg`, `.png`, `.heic`, `.gif`, `.bmp`, `.tif`, `.tiff`, `.webp`

- Video support: `.mp4`, `.mov`, `.avi`, `.mkv`, `.wmv`, `.flv`, `.webm`, `.mts`, `.m2ts`, `.3gp`

- Screenshots are placed in a separate `screenshots` folder

- Supports English and Russian screenshot names (`screenshot`, `screen`, `Снимок экрана`)

- Recursively processes all subfolders in the source directory

- Removes duplicate files by content, keeping the file in the earliest folder

---

## Требования / Requirements

- Python 3.12  
- pillow 

```bash
sudo apt install python3.12-venv
python3.12 -m venv ~/envs/gallery_sync
. ~/envs/gallery_sync/bin/activate
pip install -r requirements/requirements.txt
```

## Использование / Usage

```bash
python src/main.py <SOURCE_FOLDER> <TARGET_FOLDER>
```

### Структура организованных файлов / Output Structure

```text
TARGET_FOLDER/
├─ 2023/
│  ├─ 01/
│  │  ├─ photos/
│  │  ├─ videos/
│  │  └─ screenshots/
│  └─ 02/
│     ├─ photos/
│     ├─ videos/
│     └─ screenshots/
...
```

- Фото и видео сортируются по год/месяц
  Photos and videos are organized by year/month

- Скриншоты помещаются в папку screenshots внутри месяца
  Screenshots go into the screenshots folder inside each month

### Логика дубликатов / Duplicate Handling

- Скрипт вычисляет md5 хеш каждого файла
  The script computes md5 hash of each file

- Если файл с таким же содержимым уже существует, он пропускается
  If a file with the same content already exists, it is skipped

- Если найден файл с более ранней датой, он заменяет дубликат
  If a file with an earlier date is found, it replaces the duplicate

### Примечания / Notes

- Для фото используется дата из EXIF (если есть), иначе дата последней модификации файла
  For photos, EXIF date is used if available; otherwise, file modification date is used

- Поддерживает русские имена скриншотов в Ubuntu (Снимок экрана)
  Supports Russian screenshot names in Ubuntu (Снимок экрана)

## Лицензия / License

MIT License
