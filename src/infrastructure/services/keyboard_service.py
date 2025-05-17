from pynput import keyboard

class KeyboardService:
    def __init__(self):
        self.key_press_count = 0
        self._listener = None

    def on_press(self, key: keyboard.Key) -> None:
        self.key_press_count += 1

    def start(self) -> None:
        self._listener = keyboard.Listener(on_press=self.on_press)
        self._listener.start()

    def stop(self) -> None:
        if self._listener:
            self._listener.stop()

    def reset_counter(self) -> None:
        self.key_press_count = 0 