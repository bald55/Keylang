@echo off
set SCRIPT_DIR=%~dp0

:: Find python.exe dynamically
for /f "usebackq tokens=*" %%i in (`where python`) do (
    set "PYTHON_EXE=%%i"
    goto :found
)

:found
if not defined PYTHON_EXE (
    echo [Error] Python not found in PATH.
    pause
    exit /b 1
)

set LOGO_PATH=%SCRIPT_DIR%..\other_stuff\keylang_logo.ico
for %%i in ("%LOGO_PATH%") do set LOGO_PATH=%%~fi

assoc .kl=KeylangFile
ftype KeylangFile="%PYTHON_EXE%" "%SCRIPT_DIR%keylang_runner.py" "%%1" %%*
reg add "HKCR\KeylangFile" /ve /d "Keylang Source File" /f
reg add "HKCR\KeylangFile\DefaultIcon" /ve /d "%LOGO_PATH%" /f
reg add "HKCR\KeylangFile\shell" /ve /d "open" /f
reg add "HKCR\KeylangFile\shell\open\command" /ve /d "\"%PYTHON_EXE%\" \"%SCRIPT_DIR%keylang_runner.py\" \"%%1\"" /f

echo Keylang association installed using %PYTHON_EXE%
pause
