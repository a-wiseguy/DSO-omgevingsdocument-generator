from dataclasses import dataclass, field

from app.models import ContentType


@dataclass
class OutputFile:
    filename: str
    content_type: ContentType
    content: str
    options: dict = field(default_factory=dict)
