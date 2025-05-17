from pynput import mouse
from typing import Callable
import threading


class MouseService:
    def __init__(self):
        self.distance = 0
        self.clicks = 0
        self.scrolls = 0
        self.last_position = None
        self._listener = None
        self._lock = threading.Lock()

    def on_move(self, x: int, y: int) -> None:
        with self._lock:
            if self.last_position is not None:
                dx = x - self.last_position[0]
                dy = y - self.last_position[1]
                distance = (dx**2 + dy**2) ** 0.5 * 0.026  # conversão para cm
                self.distance += distance
            self.last_position = (x, y)

    def on_click(self, x: int, y: int, button: mouse.Button, pressed: bool) -> None:
        if pressed:
            with self._lock:
                self.clicks += 1

    def on_scroll(self, x: int, y: int, dx: int, dy: int) -> None:
        with self._lock:
            self.scrolls += 1

    def start(self) -> None:
        self._listener = mouse.Listener(
            on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll
        )
        self._listener.start()

    def stop(self) -> None:
        if self._listener:
            self._listener.stop()
            self._listener.join(timeout=1)  # Garante que o listener seja fechado

    def get_stats(self) -> dict:
        """Retorna as estatísticas atuais do mouse"""
        with self._lock:
            return {
                "quant_clicks": self.clicks,
                "quant_dist": round(self.distance, 2),
                "quant_scrow": self.scrolls
            }

    def reset_counters(self) -> None:
        with self._lock:
            self.distance = 0
            self.clicks = 0
            self.scrolls = 0
            self.last_position = None
