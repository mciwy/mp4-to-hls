@echo off

SET APP_NAME=hls_app
SET ICON_FILE=mp4tohls_icon.ico

rmdir /s /q build
rmdir /s /q dist
del %APP_NAME%.spec 2>nul

pyinstaller --noconfirm --onefile --windowed --icon=%ICON_FILE% %APP_NAME%.py

echo.
echo /dist
pause
