from abc import ABC, abstractmethod
from models import JobPosting


class JobSourceAdapter(ABC):
    """Fælles interface for alle jobkilder. Hver adapter returnerer en liste af JobPosting."""

    @abstractmethod
    def fetch(self) -> list[JobPosting]:
        ...
