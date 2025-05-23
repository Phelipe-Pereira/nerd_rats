import threading
import time
import tkinter as tk
from tkinter import simpledialog
from src.domain.entities.tracking_data import TrackingData
from src.domain.dtos.metrics_dto import MetricsDTO
from src.infrastructure.services.mouse_service import MouseService
from src.infrastructure.services.keyboard_service import KeyboardService
from src.infrastructure.services.log_service import LogService
from src.infrastructure.persistence.tracking_repository_impl import TrackingRepositoryImpl
from src.infrastructure.services.metrics_api_service_impl import MetricsApiServiceImpl
from src.infrastructure.services.stats_aggregator import StatsAggregator
from src.infrastructure.config.settings import settings


class TrackEventsUseCase:
    def __init__(self):
        self.mouse_service = MouseService()
        self.keyboard_service = KeyboardService()
        self.repository = TrackingRepositoryImpl()
        self.log_service = LogService()
        self.metrics_api_service = MetricsApiServiceImpl()
        self.running = False
        self.email = None
        self.github = None
        self.aggregator = None
        self.root = None

    def _show_input_dialog(self, title, prompt):
        """Mostra uma janela de diálogo para input"""
        if not self.root:
            self.root = tk.Tk()
            self.root.withdraw()  # Esconde a janela principal
        
        result = simpledialog.askstring(title, prompt)
        if not result:
            self.log_service.error(f"Usuário não forneceu {title.lower()}")
            raise ValueError(f"{title} é obrigatório")
        return result.strip()

    def _configure_email(self) -> None:
        self.email = settings.read_email()
        if not self.email:
            try:
                self.email = self._show_input_dialog(
                    "Email",
                    "Digite seu email para configurar o rastreamento:"
                )
                settings.save_email(self.email)
            except ValueError as e:
                self.log_service.error(str(e))
                raise
        self.log_service.info(f"Email configurado: {self.email}")

    def _configure_github(self) -> None:
        self.github = settings.read_github()
        if not self.github:
            try:
                self.github = self._show_input_dialog(
                    "GitHub",
                    "Digite seu usuário do GitHub:"
                )
                settings.save_github(self.github)
            except ValueError as e:
                self.log_service.error(str(e))
                raise
        self.log_service.info(f"GitHub configurado: {self.github}")

    def _send_metrics_to_api(self) -> None:
        metrics = MetricsDTO(
            user_github=self.github,
            email=self.email,
            quant_clicks=self.mouse_service.clicks,
            quant_dist=self.mouse_service.distance,
            quant_scrow=self.mouse_service.scrolls,
            quant_keys=self.keyboard_service.key_press_count
        )
        
        if self.metrics_api_service.send_metrics(metrics):
            # Reset counters only if metrics were sent successfully
            self.keyboard_service.reset_counter()
            self.mouse_service.reset_counters()

    def start(self) -> None:
        try:
            self._configure_email()
            self._configure_github()

            self.running = True
            self.mouse_service.start()
            self.keyboard_service.start()

            self.log_service.info("Iniciando rastreamento de eventos")

            # Configura e inicia o agregador
            self.aggregator = StatsAggregator(
                mouse_service=self.mouse_service,
                keyboard_service=self.keyboard_service,
                user_github=self.github,
                email=self.email
            )
            self.aggregator.start()

            # Inicia thread para envio de métricas para API
            self.metrics_thread = threading.Thread(target=self._metrics_loop)
            self.metrics_thread.daemon = True
            self.metrics_thread.start()

        except Exception as e:
            self.log_service.error(f"Erro ao iniciar rastreamento: {str(e)}")
            raise

    def _metrics_loop(self) -> None:
        while self.running:
            self._send_metrics_to_api()
            time.sleep(settings.INTERVAL)

    def stop(self) -> None:
        self.running = False
        if self.aggregator:
            self.aggregator.stop()
        self.mouse_service.stop()
        self.keyboard_service.stop()
        if self.root:
            self.root.destroy()
        self.log_service.info("Rastreamento de eventos finalizado")
