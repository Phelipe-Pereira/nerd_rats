import PyInstaller.__main__
import os
import sys

def build_windows_exe():
    """Gera o executável para Windows"""
    PyInstaller.__main__.run([
        'src/presentation/cli/main.py',  # Script principal
        '--name=NerdRats',               # Nome do executável
        '--onefile',                     # Gerar um único arquivo
        '--noconsole',                   # Sem console
        '--hidden-import=pynput.keyboard._win32',  # Imports necessários
        '--hidden-import=pynput.mouse._win32',
    ])

if __name__ == "__main__":
    # Instala dependências necessárias
    os.system('pip install -r requirements.txt')
    
    # Gera o executável
    build_windows_exe() 