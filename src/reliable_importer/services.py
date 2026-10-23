import logging
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from reliable_importer.exceptions import RecordValidationError
from reliable_importer.models import Product
from reliable_importer.readers import read_csv_rows
from reliable_importer.validators import parse_product

logger = logging.getLogger(__name__)

@dataclass
class ImportStatistics:
    total: int = 0
    valid: int = 0
    invalid: int = 0

def import_products(
    path: Path,
    *,
    allowed_categories: list[str],
    min_stock: int,
    skip_invalid: bool,
    statistics: ImportStatistics,
) -> Iterator[Product]:
    for line_number, row in read_csv_rows(path):
        statistics.total += 1
        try:
            product = parse_product(
                row,
                line_number=line_number,
                allowed_categories=allowed_categories,
            )
        except RecordValidationError as error:
            statistics.invalid += 1
            logger.warning(
                "Некоректний запис у рядку %s (поле %s): %s",
                error.line_number,
                error.field,
                error,
            )
            if skip_invalid:
                continue
            raise

        # Попередження про низький запас
        if product.quantity < min_stock:
            logger.warning(
                "Низький запас товару (Low Stock) ID=%s '%s': %s шт. (поріг: %s)",
                product.product_id,
                product.name,
                product.quantity,
                min_stock,
            )

        statistics.valid += 1
        yield product