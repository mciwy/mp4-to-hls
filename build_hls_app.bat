@echo off
REM === Сборка MP4 to HLS Converter ===

SET APP_NAME=hls_app
SET ICON_FILE=mp4tohls_icon.ico

REM Удаляем старые сборки
echo Очистка предыдущих сборок...
rmdir /s /q build
rmdir /s /q dist
del %APP_NAME%.spec 2>nul

REM Сборка с PyInstaller
echo Сборка .exe с иконкой...
pyinstaller --noconfirm --onefile --windowed --icon=%ICON_FILE% %APP_NAME%.py

echo.
echo ✅ Сборка завершена! Файл доступен в папке /dist
pause
