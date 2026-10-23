from pathlib import Path
import yaml
from reliable_importer.exceptions import ConfigurationError
from reliable_importer.models import AppConfig, LoggingConfig, ProcessingConfig

def load_config(path: Path) -> AppConfig:
    try:
        with path.open("r", encoding="utf-8") as file:
            raw = yaml.safe_load(file)
    except FileNotFoundError as error:
        raise ConfigurationError(f"Файл конфігурації не знайдено: {path}") from error
    except yaml.YAMLError as error:
        raise ConfigurationError("Некоректний YAML формат") from error

    try:
        config = AppConfig(
            input_path=Path(raw["input"]["path"]),
            output_path=Path(raw["output"]["path"]),
            processing=ProcessingConfig(
                min_stock=int(raw["processing"]["min_stock"]),
                allowed_categories=list(raw["processing"]["allowed_categories"]),
                skip_invalid=bool(raw["processing"]["skip_invalid"]),
            ),
            logging=LoggingConfig(
                level=str(raw["logging"]["level"]),
                path=Path(raw["logging"]["path"]),
            ),
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ConfigurationError("Структура YAML конфігурації некоректна") from error

    validate_config(config)
    return config

def validate_config(config: AppConfig) -> None:
    if config.processing.min_stock < 0:
        raise ConfigurationError("min_stock не може бути від'ємним")
    if not config.input_path.exists():
        raise ConfigurationError(f"Вхідний файл не знайдено: {config.input_path}")