@echo off
title City Bus Timetable Tuning Team - Web Interface
echo ============================================================
echo   Starting City Bus Multi-Agent Web Interface...
echo ============================================================
call "%~dp0venv\Scripts\activate.bat"
streamlit run "%~dp0app.py"
pause
