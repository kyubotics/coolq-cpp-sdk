@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass %~dp0scripts\generate.ps1 release
powershell.exe -NoProfile -ExecutionPolicy Bypass %~dp0scripts\build.ps1 release
explorer %~dp0build\release\release