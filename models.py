from dataclasses import dataclass
from datetime import datetime
import hashlib


@dataclass
class JobPosting:
    source: str
    title: str
    company: str
    location: str
    url: str
    description: str
    posted_date: str | None = None

    @property
    def id(self) -> str:
        raw = f"{self.source}:{self.url}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
