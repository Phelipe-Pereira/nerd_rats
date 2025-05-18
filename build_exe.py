import PyInstaller.__main__
import os
import sys
import shutil
from pathlib import Path


def build_windows_exe():
    """Gera o executável para Windows"""
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
        '--add-data=README.md;.',            # Inclui documentação
        f'--workpath={os.path.join("build", "temp")}',  # Diretório temporário
        f'--distpath={os.path.join("dist")}',  # Diretório de saída
        '--clean',                           # Limpa builds anteriores
    ])

    print("\nBuild concluído com sucesso!")
    print(f"Executável gerado em: {os.path.join('dist', 'NerdRats.exe')}")


if __name__ == "__main__":
    build_windows_exe() 