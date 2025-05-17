@echo off
setlocal enabledelayedexpansion

:: Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Python nao encontrado. Por favor, instale o Python 3.7 ou superior.
    exit /b 1
)

:: Cria e ativa ambiente virtual
python -m venv .venv
call .venv\Scripts\activate

:: Instala dependências
pip install -r requirements.txt

:: Cria diretório para configuração
if not exist "%APPDATA%\nerd_rats" mkdir "%APPDATA%\nerd_rats"

:: Cria arquivo .env com configurações
echo TRACKING_POST_URL=http://localhost:5000/track> .env
echo TRACKING_INTERVAL=15>> .env
echo CONFIG_PATH=%APPDATA%\nerd_rats\config.conf>> .env

:: Cria atalho na Startup para iniciar com o Windows
set STARTUP_FOLDER="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set SCRIPT_PATH="%~dp0src\presentation\cli\main.py"
set SHORTCUT="%STARTUP_FOLDER%\NerdRats.lnk"

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = %SHORTCUT% >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "pythonw.exe" >> CreateShortcut.vbs
echo oLink.Arguments = %SCRIPT_PATH% >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

echo Instalacao concluida! O programa iniciara automaticamente com o Windows.
pause
