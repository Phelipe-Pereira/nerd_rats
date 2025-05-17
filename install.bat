@echo off
setlocal enabledelayedexpansion

:: Verifica se Python 3 está instalado
python -c "import sys; assert sys.version_info[0] >= 3 and sys.version_info[1] >= 7" >nul 2>&1
if errorlevel 1 (
    echo Versao do Python incompativel. E necessario Python 3.7 ou superior.
    echo Versao atual do Python:
    python --version
    exit /b 1
)

:: Atualiza pip para a versão mais recente
python -m pip install --upgrade pip

:: Cria e ativa ambiente virtual
if exist .venv (
    rmdir /s /q .venv
)
python -m venv .venv
call .venv\Scripts\activate
if errorlevel 1 (
    echo Erro ao ativar ambiente virtual
    exit /b 1
)

:: Instala dependências
pip install -r requirements.txt
if errorlevel 1 (
    echo Erro ao instalar dependencias
    exit /b 1
)

:: Cria diretório para configuração
if not exist "%APPDATA%\nerd_rats" mkdir "%APPDATA%\nerd_rats"

:: Cria arquivo .env com configurações
echo TRACKING_POST_URL=http://localhost:5000/track> .env
echo TRACKING_INTERVAL=15>> .env
echo CONFIG_PATH=%APPDATA%\nerd_rats\config.conf>> .env

:: Cria atalho na Startup para iniciar com o Windows
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "VENV_PYTHON=%~dp0.venv\Scripts\pythonw.exe"
set "SCRIPT_PATH=%~dp0src\presentation\cli\main.py"
set "SHORTCUT=%STARTUP_FOLDER%\NerdRats.lnk"

:: Verifica se os arquivos necessários existem
if not exist "%VENV_PYTHON%" (
    echo Erro: Python do ambiente virtual nao encontrado
    exit /b 1
)
if not exist "%SCRIPT_PATH%" (
    echo Erro: Script principal nao encontrado
    exit /b 1
)

:: Cria o script VBS para criar o atalho
(
    echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
    echo sLinkFile = "%SHORTCUT%"
    echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
    echo oLink.TargetPath = "%VENV_PYTHON%"
    echo oLink.Arguments = "%SCRIPT_PATH%"
    echo oLink.WorkingDirectory = "%~dp0"
    echo oLink.Save
) > CreateShortcut.vbs

cscript //nologo CreateShortcut.vbs
if errorlevel 1 (
    echo Erro ao criar atalho
    del CreateShortcut.vbs
    exit /b 1
)
del CreateShortcut.vbs

echo Instalacao concluida! O programa iniciara automaticamente com o Windows.
pause
