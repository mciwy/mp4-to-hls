# 🎬 MP4 to HLS Converter (Desktop App)

Простое и удобное десктопное приложение для Windows, позволяющее конвертировать `.mp4` видеофайлы в потоковый формат **HLS** (`.m3u8` + `.ts`) с поддержкой нескольких разрешений и автообновлением.

---

## 📦 Возможности

- ✅ Поддержка 3 потоков: **480p**, **720p**, **1080p**
- ✏️ Настраиваемые битрейты
- 📁 Выбор входного видео и выходной папки
- 📜 Генерация `.txt`-лога после конвертации
- 💾 Сохранение последних путей и настроек

---

## 🚀 Скачать .exe

👉 [Скачать последнюю версию (.exe)](https://github.com/mciwy/mp4-to-hls/releases/latest)

---

## 🔄 Автообновление

Приложение автоматически проверяет наличие новой версии при запуске.  
Если обновление доступно — предлагает скачать с GitHub.

---

## 🖥️ Интерфейс

<img src="https://github.com/mciwy/mp4-to-hls/assets/preview.png" alt="Превью интерфейса" width="600"/>

---

## 🛠️ Сборка вручную (.exe)

> Требуется: Python 3.10+, [FFmpeg](https://ffmpeg.org/), [PyInstaller](https://pyinstaller.org/)

### 1. Установить зависимости

```bash
pip install pyinstaller
```

### 2. Использовать скрипт сборки

Файл: [`build_hls_app.bat`](build_hls_app.bat)

Он:
- удаляет старые сборки
- собирает `.exe`

```bash
pyinstaller --noconfirm --onefile --windowed --icon=mp4tohls_icon.ico hls_app.py
```

---

## 🧩 Структура проекта

```
mp4-to-hls/
├── hls_app.py              # Основной код
├── mp4tohls_icon.ico       # Иконка для .exe
├── build_hls_app.bat       # Сборка .exe
├── version.json            # Для автообновления
├── README.md               # Документация
├── .gitignore
└── dist/                   # Готовый .exe (после сборки)
```

---

## 🧑‍💻 Автор

**@deliorix aka @mciwy**  
