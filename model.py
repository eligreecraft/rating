from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ReportEntry:
    name: str
    url: str
    likes: int
    comments: int
    balls: int
    used: int


class Report:
    def __init__(self):
        self.entries = []
        self.generated_at = datetime.utcnow().replace(microsecond=0)
        self.generated_at_iso_8601 = f"{self.generated_at.isoformat()}Z"

    def add(
        self, name: str, url: str, likes: int, comments: int, balls: int, used: int
    ):
        self.entries.append(
            ReportEntry(
                name=name,
                url=url,
                likes=likes,
                comments=comments,
                balls=balls,
                used=used if used else 0,
            )
        )
