@echo off
title City Bus Timetable Tuning Team - Terminal Mode
echo ============================================================
echo   Running City Bus Multi-Agent System (Terminal Mode)...
echo ============================================================
call "%~dp0venv\Scripts\activate.bat"
python "%~dp0main.py"
pause
