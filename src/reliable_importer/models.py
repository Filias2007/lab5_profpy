from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True, slots=True)
class Product:
    product_id: int
    name: str
    category: str
    price: float
    quantity: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

@dataclass(frozen=True, slots=True)
class ProcessingConfig:
    min_stock: int
    allowed_categories: list[str]
    skip_invalid: bool

@dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str
    path: Path

@dataclass(frozen=True, slots=True)
class AppConfig:
    input_path: Path
    output_path: Path
    processing: ProcessingConfig
    logging: LoggingConfig