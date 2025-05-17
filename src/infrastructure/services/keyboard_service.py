from pynput import keyboard
import threading


class KeyboardService:
    def __init__(self):
        self.key_press_count = 0
        self._listener = None
        self._lock = threading.Lock()

    def on_press(self, key: keyboard.Key) -> None:
        with self._lock:
            self.key_press_count += 1

    def start(self) -> None:
        self._listener = keyboard.Listener(on_press=self.on_press)
        self._listener.start()

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
