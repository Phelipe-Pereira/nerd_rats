import signal
import sys
import os
import tempfile
import atexit

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.application.use_cases.track_events_use_case import TrackEventsUseCase

# Arquivo de lock para garantir instância única
LOCK_FILE = os.path.join(tempfile.gettempdir(), "nerdrats.lock")

def cleanup():
    """Remove o arquivo de lock ao fechar o programa"""
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
    except:
        pass

def is_running():
    """Verifica se já existe uma instância do programa rodando"""
    try:
        if os.path.exists(LOCK_FILE):
            # Verifica se o processo ainda está rodando
            with open(LOCK_FILE, 'r') as f:
                pid = int(f.read().strip())
                try:
                    os.kill(pid, 0)  # Verifica se o processo existe
                    return True
                except OSError:
                    pass  # Processo não existe mais
        
        # Cria arquivo de lock
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        
        # Registra função de cleanup
        atexit.register(cleanup)
        return False
    except:
        return False

def main():
    # Verifica se já existe uma instância rodando
    if is_running():
        print("NerdRats já está rodando!")
        sys.exit(1)

    tracker = TrackEventsUseCase()

    def signal_handler(signum, frame):
        print("\nEncerrando o rastreamento...")
        tracker.stop()
        cleanup()
        sys.exit(0)

    # Registra handler para Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Iniciando rastreamento de eventos...")
    tracker.start()

    # Mantém o programa rodando
    try:
        signal.pause()
    except AttributeError:  # Windows não tem signal.pause()
        while True:
            pass


if __name__ == "__main__":
    main()
