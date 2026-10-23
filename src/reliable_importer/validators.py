from reliable_importer.exceptions import RecordValidationError
from reliable_importer.models import Product

def parse_product(
    row: dict[str, str],
    *,
    line_number: int,
    allowed_categories: list[str],
) -> Product:
    # 1. product_id
    try:
        product_id = int(row["product_id"])
        if product_id <= 0:
            raise ValueError
    except (KeyError, TypeError, ValueError) as error:
        raise RecordValidationError(
            "product_id має бути додатним цілим числом",
            line_number=line_number,
            field="product_id",
        ) from error

    # 2. name
    name = row.get("name", "").strip()
    if not name:
        raise RecordValidationError(
            "Назва товару порожня",
            line_number=line_number,
            field="name",
        )

    # 3. category
    category = row.get("category", "").strip()
    if category not in allowed_categories:
        raise RecordValidationError(
            f"Категорія '{category}' не дозволена",
            line_number=line_number,
            field="category",
        )

    # 4. price
    try:
        price = float(row["price"])
        if price < 0:
            raise ValueError
    except (KeyError, TypeError, ValueError) as error:
        raise RecordValidationError(
            "Ціна має бути невід'ємним числом (>= 0)",
            line_number=line_number,
            field="price",
        ) from error

    # 5. quantity
    try:
        quantity = int(row["quantity"])
        if quantity < 0:
            raise ValueError
    except (KeyError, TypeError, ValueError) as error:
        raise RecordValidationError(
            "Кількість має бути невід'ємним цілим числом (>= 0)",
            line_number=line_number,
            field="quantity",
        ) from error

    return Product(
        product_id=product_id,
        name=name,
        category=category,
        price=price,
        quantity=quantity,
    )