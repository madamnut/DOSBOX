@echo off
setlocal

rem Builder.bat is inside ORIGIN\src
rem Move to the folder where this batch file exists
cd /d "%~dp0"

rem Build main.asm into ..\ORIGIN.COM
nasm -f bin main.asm -o ..\ORIGIN.COM

if errorlevel 1 (
echo.
echo Build failed.
pause
exit /b 1
)

echo.
echo Build succeeded: ..\ORIGIN.COM
pause
