@echo off
chcp 65001 > nul
title War Thunder Rich Presence

:: Включаем поддержку ANSI цветов
set ENABLE_VIRTUAL_TERMINAL_PROCESSING=1

echo  War Thunder Discord Rich Presence v1.1.0 (Release)
echo.

py main.py

pause