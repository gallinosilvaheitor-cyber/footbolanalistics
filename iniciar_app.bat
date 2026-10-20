@echo off
chcp 65001 > nul
title Football Analytics Hub — Inicializador

cd /d "%~dp0"
python launcher.py

if %errorlevel% neq 0 (
    echo.
    echo Ocorreu um erro ao iniciar o aplicativo com o comando python.
    echo Tentando com o inicializador 'py'...
    py launcher.py
    pause
)
