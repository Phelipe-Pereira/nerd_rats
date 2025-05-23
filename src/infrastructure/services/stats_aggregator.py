import threading
import time
from typing import Dict
from src.infrastructure.services.mouse_service import MouseService
from src.infrastructure.services.keyboard_service import KeyboardService
from src.infrastructure.services.log_service import LogService
from src.infrastructure.config.settings import settings


class StatsAggregator:
    def __init__(self, mouse_service: MouseService, keyboard_service: KeyboardService,
                 user_github: str, email: str):
        self.mouse_service = mouse_service
        self.keyboard_service = keyboard_service
        self.user_github = user_github
        self.email = email
        self.running = False
        self._aggregation_thread = None
        self._lock = threading.Lock()
        self.log_service = LogService()
        self._print_client_info()

    def _print_client_info(self) -> None:
        self.log_service.info("=== Informações do Cliente ===")
        self.log_service.info(f"GitHub: {self.user_github}")
        self.log_service.info(f"Email: {self.email}")
        self.log_service.info("============================")

    def _aggregate_and_send(self) -> None:
        while self.running:
            try:
                # Aguarda o intervalo antes de coletar
                time.sleep(settings.INTERVAL)

                with self._lock:
                    # Coleta estatísticas
                    mouse_stats = self.mouse_service.get_stats()
                    keyboard_stats = self.keyboard_service.get_stats()

                    # Combina as estatísticas
                    stats = {
                        "user_github": self.user_github,
                        "email": self.email,
                        **mouse_stats,
                        **keyboard_stats
                    }

                self.log_service.info("=== Dados do Cliente ===")
                self.log_service.info(f"GitHub: {self.user_github}")
                self.log_service.info(f"Email: {self.email}")
                self.log_service.info("=== Estatísticas Coletadas ===")
                self.log_service.info(f"Clicks: {stats.get('quant_clicks', 0)}")
                self.log_service.info(f"Distância do mouse: {stats.get('quant_dist', 0):.2f}cm")
                self.log_service.info(f"Scrolls: {stats.get('quant_scrow', 0)}")
                self.log_service.info(f"Teclas pressionadas: {stats.get('quant_keys', 0)}")
                self.log_service.info("============================")

            except Exception as e:
                self.log_service.error(f"Erro ao coletar estatísticas: {str(e)}")
                time.sleep(settings.INTERVAL)

    def start(self) -> None:
        """Inicia o agregador de estatísticas"""
        with self._lock:
            self.running = True
            self._aggregation_thread = threading.Thread(target=self._aggregate_and_send, daemon=True)
            self._aggregation_thread.start()
            self.log_service.info("Agregador de estatísticas iniciado")

    def stop(self) -> None:
        """Para o agregador de estatísticas"""
        with self._lock:
            self.running = False
            if self._aggregation_thread:
                self._aggregation_thread.join(timeout=1)
            self.log_service.info("Agregador de estatísticas parado")