import PyInstaller.__main__
import os
import sys
from pathlib import Path
import subprocess


def create_env_example():
    """Cria o arquivo .env.example com configurações padrão"""
    env_content = """TRACKING_POST_URL=https://nerds-rats-hackathon.onrender.com/metrics
TRACKING_INTERVAL=60
LOG_LEVEL=INFO
LOG_RETENTION_DAYS=30"""
    
    with open(".env.example", "w") as f:
        f.write(env_content)


def check_input_permissions():
    """Verifica e configura permissões necessárias para captura de eventos"""
    try:
        # Verifica se o usuário atual está no grupo input
        result = subprocess.run(['groups'], capture_output=True, text=True)
        if 'input' not in result.stdout:
            print("\nAVISO: Usuário não está no grupo 'input'. Isso pode afetar a captura de eventos.")
            print("Para corrigir, execute como root:")
            print("usermod -a -G input $USER")
            print("E faça logout e login novamente.\n")
    except Exception as e:
        print(f"Erro ao verificar permissões: {e}")


def build_linux_exe():
    """Gera o executável para Linux"""
    # Verifica permissões
    check_input_permissions()

    # Cria .env.example se não existir
    if not os.path.exists(".env.example"):
        create_env_example()

    # Cria diretório para logs
    log_dir = "/var/log/nerd_rats"
    if not os.path.exists(log_dir):
        print(f"AVISO: O diretório {log_dir} será criado na primeira execução")

    # Configurações do PyInstaller
    PyInstaller.__main__.run([
        'src/presentation/cli/main.py',      # Script principal
        '--name=NerdRats',                   # Nome do executável
        '--onefile',                         # Gerar um único arquivo
        '--noconsole',                       # Sem console
        '--hidden-import=pynput.keyboard._xorg',  # Imports necessários
        '--hidden-import=pynput.mouse._xorg',
        '--add-data=.env.example:.',         # Inclui arquivo de exemplo
        '--add-data=README.md:.',            # Inclui documentação
        f'--workpath={os.path.join("build", "temp")}',  # Diretório temporário
        f'--distpath={os.path.join("dist")}',  # Diretório de saída
        '--clean',                           # Limpa builds anteriores
    ])

    print("\nBuild concluído com sucesso!")
    print(f"Executável gerado em: {os.path.join('dist', 'NerdRats')}")
    print("\nPara executar:")
    print("1. Dê permissão de execução: chmod +x ./NerdRats")
    print("2. Execute como root: sudo ./NerdRats")
    print("\nSe a captura de eventos não funcionar:")
    print("1. Adicione seu usuário ao grupo input: sudo usermod -a -G input $USER")
    print("2. Faça logout e login")
    print("3. Execute novamente: sudo ./NerdRats")


if __name__ == "__main__":
    if os.name != "posix":
        print("Este script deve ser executado em um sistema Linux")
        sys.exit(1)
    build_linux_exe() 