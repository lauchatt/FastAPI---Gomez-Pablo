CATEGORIES: list[dict[str, str]] = [
    {
        "name": "ciencia",
        "label": "Science and technology",
        "description": (
            "Questions about natural sciences, physics, chemistry, biology, "
            "astronomy, medicine, technology, inventions, scientific discoveries, "
            "and how things work."
        ),
        "dataset_config": "science-technology",
    },

    {
        "name": "geografia",
        "label": "Geography and places",
        "description": (
            "Questions about countries, capitals, cities, continents, "
            "mountains, rivers, oceans, borders, maps, and locations."
        ),
        "dataset_config": "geography",
    },

    {
        "name": "historia",
        "label": "History and historical events",
        "description": (
            "Questions about historical events, dates, wars, civilizations, "
            "historical periods, rulers, and important historical figures."
        ),
        "dataset_config": "history",
    },

    {
        "name": "deporte",
        "label": "Sports and sporting events",
        "description": (
            "Questions about sports, athletes, teams, competitions, "
            "tournaments, championships, records, rules, and sporting events."
        ),
        "dataset_config": "sports",
    },

    {
        "name": "arte",
        "label": "Arts, literature, and humanities",
        "description": (
            "Questions about painting, sculpture, architecture, literature, "
            "poetry, philosophy, artists, writers, art movements, and humanities."
        ),
        "dataset_config": "humanities",
    },

    {
        "name": "entretenimiento",
        "label": "Entertainment and popular culture",
        "description": (
            "Questions about movies, television, music, actors, singers, "
            "celebrities, fictional characters, video games, and popular culture."
        ),
        "dataset_config": "entertainment",
    },
]


def get_category_names() -> list[str]:
    return [category["name"] for category in CATEGORIES]


def get_category_labels() -> list[str]:
    return [category["label"] for category in CATEGORIES]


def get_category_descriptions() -> list[str]:
    return [category["description"] for category in CATEGORIES]


def find_category_by_name(name: str) -> dict[str, str] | None:
    for category in CATEGORIES:
        if category["name"] == name:
            return category
    return None