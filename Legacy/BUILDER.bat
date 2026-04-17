@echo off
setlocal

cd /d "%~dp0"

set BUILD_FAILED=0

for %%F in (*.asm) do (
    echo.
    echo Building %%F ...

    nasm -f bin "%%F" -o "%%~nF.com"
    if errorlevel 1 (
        echo FAILED: %%F
        set BUILD_FAILED=1
    ) else (
        echo SUCCESS: %%F ^> %%~nF.com
    )
)

echo.
if "%BUILD_FAILED%"=="1" (
    echo ======================
    echo      BUILD FAILED
    echo ======================
) else (
    echo ======================
    echo     BUILD SUCCESS
    echo ======================
)

echo.
pause