# Лабораторна робота №5: Обробка помилок, файли та серіалізація
**Варіант 3:** Імпорт та експорт даних інтернет-магазину

## Опис проєкту
Модуль призначений для надійного імпорту даних про товари з CSV-файлу, їхньої валідації, фільтрації, логування попереджень (зокрема про низький запас товару) та атомарного експорту у формат JSON.

## Структура папки LAB_05
```text
LAB_05/
├── config.yaml
├── pyproject.toml
├── README.md
├── data/
│   └── products.csv
├── output/
│   └── products.json
├── logs/
│   └── application.log
└── src/
    └── reliable_importer/
        ├── __init__.py
        ├── main.py
        ├── config.py
        ├── exceptions.py
        ├── models.py
        ├── readers.py
        ├── validators.py
        ├── exporters.py
        ├── logging_config.py
        ├── services.py
        └── utils.py