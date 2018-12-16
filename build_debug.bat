@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass %~dp0scripts\generate.ps1 debug
powershell.exe -NoProfile -ExecutionPolicy Bypass %~dp0scripts\build.ps1 debug
explorer %~dp0build\debug\debug