import threading
import time
from typing import Dict
from src.infrastructure.services.mouse_service import MouseService
from src.infrastructure.services.keyboard_service import KeyboardService
from src.infrastructure.persistence.tracking_repository_impl import TrackingRepositoryImpl
from src.infrastructure.services.log_service import LogService
from src.domain.entities.tracking_data import TrackingData


class StatsAggregator:
    def __init__(self, mouse_service: MouseService, keyboard_service: KeyboardService, 
                 repository: TrackingRepositoryImpl, user_github: str, email: str):
        self.mouse_service = mouse_service
        self.keyboard_service = keyboard_service
        self.repository = repository
        self.user_github = user_github
        self.email = email
        self.running = False
        self._aggregation_thread = None
        self.log_service = LogService()
        self._print_client_info()

    def _print_client_info(self) -> None:
        self.log_service.info("=== Informações do Cliente ===")
        self.log_service.info(f"GitHub: {self.user_github}")
        self.log_service.info(f"Email: {self.email}")
        self.log_service.info("============================")

    def _aggregate_and_send(self) -> None:
        while self.running:
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

            # Cria objeto de tracking
            tracking_data = TrackingData(
                email=self.email,
                keys_pressed=keyboard_stats["quant_keys"],
                mouse_distance_cm=mouse_stats["quant_dist"],
                clicks=mouse_stats["quant_clicks"],
                scrolls=mouse_stats["quant_scrow"]
            )

            # Tenta enviar os dados
            success = self.repository.send_tracking_data(tracking_data)
            if success:
                self.log_service.info("✓ Dados enviados com sucesso!")
            else:
                self.log_service.warning("✗ Falha ao enviar dados - salvos no cache local")

            # Reseta os contadores
            self.mouse_service.reset_counters()
            self.keyboard_service.reset_counter()

            # Aguarda
            self.log_service.info("Aguardando 20 segundos para próxima coleta...")
            time.sleep(20)

    def start(self) -> None:
        """Inicia o agregador de estatísticas"""
        self.running = True
        self._aggregation_thread = threading.Thread(target=self._aggregate_and_send, daemon=True)
        self._aggregation_thread.start()
        self.log_service.info("Agregador de estatísticas iniciado")

    def stop(self) -> None:
        """Para o agregador de estatísticas"""
        self.running = False
        if self._aggregation_thread:
            self._aggregation_thread.join(timeout=1)
        self.log_service.info("Agregador de estatísticas parado") 