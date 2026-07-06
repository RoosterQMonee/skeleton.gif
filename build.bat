@echo off

gcc ^
    -std=c17 ^
    -O2 ^
    -s ^
    -Wall ^
    -Wextra ^
    -pedantic ^
    -DWIN32_LEAN_AND_MEAN ^
    -mwindows ^
    -o overlay.exe ^
    src/main.c ^
    -lgdi32 ^
    -luser32 ^
    -lwinmm

if errorlevel 1 (
    echo.
    echo Build failed.
    exit /b 1
)

echo.
echo Build complete:
echo   overlay.exe