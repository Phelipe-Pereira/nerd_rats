from pynput import keyboard
import threading
import sys
import os


class KeyboardService:
    def __init__(self):
        self.key_press_count = 0
        self._listener = None
        self._lock = threading.Lock()
        self._configure_python_path()

    def _configure_python_path(self) -> None:
        """Configura o caminho do Python para o pynput"""
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            # Estamos em um ambiente virtual
            python_path = os.path.join(sys.prefix, 'python.exe' if os.name == 'nt' else 'python')
            if os.path.exists(python_path):
                os.environ['PYTHONEXECUTABLE'] = python_path

    def on_press(self, key: keyboard.Key) -> None:
        with self._lock:
            self.key_press_count += 1

    def start(self) -> None:
        try:
            self._listener = keyboard.Listener(on_press=self.on_press)
            self._listener.start()
        except Exception as e:
            print(f"Erro ao iniciar o listener do teclado: {str(e)}")
            raise

    def stop(self) -> None:
        if self._listener:
            self._listener.stop()
            self._listener.join(timeout=1)  # Garante que o listener seja fechado

    def get_stats(self) -> dict:
        """Retorna as estatísticas atuais do teclado"""
        with self._lock:
            return {
                "quant_keys": self.key_press_count
            }

    def reset_counter(self) -> None:
        with self._lock:
            self.key_press_count = 0
