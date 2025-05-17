import threading
import time
from typing import Dict
from src.infrastructure.services.mouse_service import MouseService
from src.infrastructure.services.keyboard_service import KeyboardService
from src.infrastructure.persistence.tracking_repository_impl import TrackingRepositoryImpl
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
        self._print_client_info()

    def _print_client_info(self) -> None:
        print("\n=== Informações do Cliente ===")
        print(f"GitHub: {self.user_github}")
        print(f"Email: {self.email}")
        print("============================\n")

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

            print("\n=== Dados do Cliente ===")
            print(f"GitHub: {self.user_github}")
            print(f"Email: {self.email}")
            print("\n=== Estatísticas Coletadas ===")
            print(f"Clicks: {stats.get('quant_clicks', 0)}")
            print(f"Distância do mouse: {stats.get('quant_dist', 0):.2f}cm")
            print(f"Scrolls: {stats.get('quant_scrow', 0)}")
            print(f"Teclas pressionadas: {stats.get('quant_keys', 0)}")
            print("============================\n")

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
                print("✓ Dados enviados com sucesso!")
            else:
                print("✗ Falha ao enviar dados - salvos no cache local")

            # Reseta os contadores
            self.mouse_service.reset_counters()
            self.keyboard_service.reset_counter()

            # Aguarda
            print("\nAguardando 20 segundos para próxima coleta...")
            time.sleep(20)

    def start(self) -> None:
        """Inicia o agregador de estatísticas"""
        self.running = True
        self._aggregation_thread = threading.Thread(target=self._aggregate_and_send, daemon=True)
        self._aggregation_thread.start()

    def stop(self) -> None:
        """Para o agregador de estatísticas"""
        self.running = False
        if self._aggregation_thread:
            self._aggregation_thread.join(timeout=1) 