import threading
import time
from src.domain.entities.tracking_data import TrackingData
from src.infrastructure.services.mouse_service import MouseService
from src.infrastructure.services.keyboard_service import KeyboardService
from src.infrastructure.persistence.tracking_repository_impl import (
    TrackingRepositoryImpl,
)
from src.infrastructure.services.stats_aggregator import StatsAggregator
from src.infrastructure.config.settings import settings


class TrackEventsUseCase:
    def __init__(self):
        self.mouse_service = MouseService()
        self.keyboard_service = KeyboardService()
        self.repository = TrackingRepositoryImpl()
        self.running = False
        self.email = None
        self.aggregator = None

    def _configure_email(self) -> None:
        self.email = settings.read_email()
        if not self.email:
            self.email = input(
                "Digite seu email para configurar o rastreamento: "
            ).strip()
            settings.save_email(self.email)

    def _configure_github(self) -> None:
        self.github = settings.read_github()
        if not self.github:
            self.github = input(
                "Digite seu usuário do GitHub: "
            ).strip()
            settings.save_github(self.github)

    def start(self) -> None:
        self._configure_email()
        self._configure_github()

        self.running = True
        self.mouse_service.start()
        self.keyboard_service.start()

        # Configura e inicia o agregador
        self.aggregator = StatsAggregator(
            mouse_service=self.mouse_service,
            keyboard_service=self.keyboard_service,
            repository=self.repository,
            user_github=self.github,
            email=self.email
        )
        self.aggregator.start()

    def stop(self) -> None:
        self.running = False
        if self.aggregator:
            self.aggregator.stop()
        self.mouse_service.stop()
        self.keyboard_service.stop()
