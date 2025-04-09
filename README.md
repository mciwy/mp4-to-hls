# MP4 to HLS Converter (Desktop App)

Простое десктопное приложение для конвертации MP4-видео в HLS-поток с поддержкой 480p, 720p и 1080p.

## 🔧 Возможности

- Выбор MP4-файла и выходной директории
- Поддержка трёх разрешений
- Ручной ввод битрейтов
- Лог-файл после конвертации (`conversion_log.txt`)
- Прогрессбар
- Сохранение последнего состояния и путей (`config.json`)

## 💻 Зависимости

- Python 3.10+
- FFmpeg (должен быть доступен через `PATH`)

## 🚀 Запуск

```bash
python hls_app.py
