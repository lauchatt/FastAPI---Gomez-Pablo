"""
Definición de las categorías utilizadas por el clasificador.
"""

CATEGORIES: list[dict[str, str]] = [
    {
        "name": "ciencia",
        "label": "Science and technology questions",
        "description": "Questions about science, technology, scientific discoveries, and how things work.",
        "dataset_config": "science-technology",
    },
    {
        "name": "geografia",
        "label": "Geography questions about countries, capitals, and places",
        "description": "Questions about countries, capitals, mountains, rivers, and world geography.",
        "dataset_config": "geography",
    },
    {
        "name": "historia",
        "label": "History questions about past events and figures",
        "description": "Questions about historical events, dates, wars, and important historical figures.",
        "dataset_config": "history",
    },
    {
        "name": "deporte",
        "label": "Sports questions about athletes, teams, and competitions",
        "description": "Questions about sports, athletes, teams, rules, and sporting events.",
        "dataset_config": "sports",
    },
    {
        "name": "arte",
        "label": "Art and humanities questions",
        "description": "Questions about art, artists, literature, philosophy, and humanities topics.",
        "dataset_config": "humanities",
    },
    {
        "name": "entretenimiento",
        "label": "Entertainment questions about movies, music, and pop culture",
        "description": "Questions about movies, music, television, and general entertainment and pop culture.",
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