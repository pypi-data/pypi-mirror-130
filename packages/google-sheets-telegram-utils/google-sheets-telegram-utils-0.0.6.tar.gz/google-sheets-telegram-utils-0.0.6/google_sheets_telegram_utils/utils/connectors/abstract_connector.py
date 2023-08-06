from abc import ABC, abstractmethod

from google_sheets_telegram_utils.utils.configs.abstract_config import AbstractConfig


class AbstractConnector(ABC):
    def __init__(self, config: AbstractConfig):
        self.config = config

    @abstractmethod
    def get_data(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def add_rows(self, rows: list) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_row(self, row):
        raise NotImplementedError

    @abstractmethod
    def get_row_by_id(self, pk) -> dict:
        raise NotImplementedError