import PyInstaller.__main__
import os
import sys
import shutil
from pathlib import Path


def create_env_example():
    """Cria o arquivo .env.example com configurações padrão"""
    env_content = """TRACKING_POST_URL=https://nerds-rats-hackathon.onrender.com/metrics
TRACKING_INTERVAL=60
LOG_LEVEL=INFO
LOG_RETENTION_DAYS=30"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)


def build_windows_exe():
    """Gera o executável para Windows"""
    # Cria .env.example se não existir
    if not os.path.exists(".env.example"):
        create_env_example()

    # Cria diretório para logs
    log_dir = os.path.join(os.getenv("APPDATA"), "nerd_rats", "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Configurações do PyInstaller
    PyInstaller.__main__.run([
        'src/presentation/cli/main.py',      # Script principal
        '--name=NerdRats',                   # Nome do executável
        '--onefile',                         # Gerar um único arquivo
        '--noconsole',                       # Sem console
        '--hidden-import=pynput.keyboard._win32',  # Imports necessários
        '--hidden-import=pynput.mouse._win32',
        '--add-data=.env.example;.',         # Inclui arquivo de exemplo
        '--add-data=README.md;.',            # Inclui documentação
        '--icon=assets/icon.ico',            # Ícone do executável
        f'--workpath={os.path.join("build", "temp")}',  # Diretório temporário
        f'--distpath={os.path.join("dist")}',  # Diretório de saída
        '--clean',                           # Limpa builds anteriores
    ])

    print("\nBuild concluído com sucesso!")
    print(f"Executável gerado em: {os.path.join('dist', 'NerdRats.exe')}")


if __name__ == "__main__":
    build_windows_exe() 