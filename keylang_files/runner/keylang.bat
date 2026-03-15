@echo off
set SCRIPT_DIR=%~dp0

:: Path to bundled Python
set "PYTHON_EXE=%SCRIPT_DIR%..\other_stuff\pypy\pypy3.exe"

if not exist "%PYTHON_EXE%" (
    echo [Error] Bundled Python not found at:
    echo %PYTHON_EXE%
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

echo Keylang association installed :D
echo %PYTHON_EXE%
pause
