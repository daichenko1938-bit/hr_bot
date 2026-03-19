def normalize_text(value: str) -> str:
    """
    Приводит текст к нижнему регистру и убирает лишние пробелы.
    """
    if not value:
        return ""
    return " ".join(value.strip().lower().split())


def normalize_city(city: str) -> str:
    """
    Нормализация города.
    Например: Орел -> орёл
    """
    city = normalize_text(city)

    city_aliases = {
        "орел": "орёл",
        "orel": "орёл",
        "москва": "москва",
        "moscow": "москва",
        "спб": "санкт-петербург",
        "питер": "санкт-петербург",
        "saint petersburg": "санкт-петербург",
    }

    return city_aliases.get(city, city)


def normalize_profession(profession: str) -> str:
    """
    Нормализация профессии.
    Сводим похожие названия к одному виду.
    """
    profession = normalize_text(profession)

    profession_aliases = {
        "продавец-консультант": "продавец",
        "кассир-продавец": "продавец",
        "менеджер по продажам": "менеджер по продажам",
        "sales manager": "менеджер по продажам",
        "кладовщик-комплектовщик": "кладовщик",
        "водитель-экспедитор": "водитель",
        "бухгалтер по расчету зарплаты": "бухгалтер",
    }

    return profession_aliases.get(profession, profession)