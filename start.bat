@echo off
chcp 65001 > nul
title War Thunder Rich Presence

:: Включаем поддержку ANSI цветов
set ENABLE_VIRTUAL_TERMINAL_PROCESSING=1

py main.py

pause