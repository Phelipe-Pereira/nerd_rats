import signal
import sys
import os
import sys

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.application.use_cases.track_events_use_case import TrackEventsUseCase

def main():
    tracker = TrackEventsUseCase()

    def signal_handler(signum, frame):
        print("\nEncerrando o rastreamento...")
        tracker.stop()
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