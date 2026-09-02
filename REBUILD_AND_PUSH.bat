@echo off
title Municipal Portfolio - Rebuild and Push
cd /d "%~dp0"
echo Repository: %CD%
echo Starting the portfolio builder. Keep this window open.
echo.
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -NoExit -File "%~dp0update-github.ps1"
