import logging
from pathlib import Path
from reliable_importer.config import load_config
from reliable_importer.exceptions import ApplicationError
from reliable_importer.exporters import export_products_json
from reliable_importer.logging_config import configure_logging
from reliable_importer.services import ImportStatistics, import_products
from reliable_importer.utils import logged_operation

logger = logging.getLogger(__name__)

def main() -> None:
    try:
        config = load_config(Path("config.yaml"))
        configure_logging(config.logging.level, config.logging.path)

        statistics = ImportStatistics()

        with logged_operation("Імпорт та Експорт Товарів"):
            products = import_products(
                config.input_path,
                allowed_categories=config.processing.allowed_categories,
                min_stock=config.processing.min_stock,
                skip_invalid=config.processing.skip_invalid,
                statistics=statistics,
            )

            exported_count = export_products_json(products, config.output_path)

        logger.info(
            "Статистика: Усього=%s, Валідні=%s, Невалідні=%s, Експортовано=%s",
            statistics.total,
            statistics.valid,
            statistics.invalid,
            exported_count,
        )

    except ApplicationError as error:
        logger.error("Критична помилка застосунку: %s", error)
        raise SystemExit(1) from error

if __name__ == "__main__":
    main()