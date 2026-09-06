"""
Definición de las categorías utilizadas por el clasificador.
"""

CATEGORIES: list[dict[str, str]] = [
    {
        "name": "blocks",
        "label": "Minecraft blocks, building materials, and block properties",
        "description": (
            "Questions about Minecraft blocks, building materials, "
            "and block properties."
        ),
    },
    {
        "name": "items",
        "label": (
            "Minecraft items, tools, weapons, armor, food, ingredients, "
            "potions, and usable resources"
        ),
        "description": (
            "Questions about Minecraft items, tools, weapons, armor, food, "
            "ingredients, potions, and usable resources."
        ),
    },
    {
        "name": "mobs",
        "label": (
            "Minecraft mobs, creatures, their behavior, spawning, combat, "
            "and drops"
        ),
        "description": (
            "Questions about Minecraft mobs and creatures, including their "
            "behavior, spawning, combat, and drops."
        ),
    },
    {
        "name": "world",
        "label": (
            "Minecraft biomes, dimensions, structures, terrain, "
            "world generation, caves, oceans, and exploration"
        ),
        "description": (
            "Questions about Minecraft biomes, dimensions, structures, "
            "terrain, world generation, caves, oceans, and exploration."
        ),
    },
    {
        "name": "redstone",
        "label": (
            "Minecraft redstone, mechanisms, circuits, components, "
            "and redstone contraptions"
        ),
        "description": (
            "Questions about Minecraft redstone, mechanisms, circuits, "
            "components, and redstone contraptions."
        ),
    },
    {
        "name": "commands",
        "label": (
            "Minecraft commands, command syntax, command blocks, "
            "and command-related mechanics"
        ),
        "description": (
            "Questions about Minecraft commands, command syntax, command "
            "blocks, and command-related mechanics."
        ),
    },
    {
        "name": "tutorials",
        "label": (
            "Minecraft tutorials, tutorial hints, controls, HUD, "
            "interface, and instructions for learning how to play"
        ),
        "description": (
            "Questions about Minecraft tutorials, tutorial hints, controls, "
            "HUD, interface, and instructions for learning how to play."
        ),
    },
    {
        "name": "gameplay",
        "label": (
            "Minecraft gameplay mechanics, inventory, trading, progression, "
            "achievements, statistics, and general game rules"
        ),
        "description": (
            "Questions about Minecraft gameplay mechanics, inventory, "
            "trading, progression, achievements, statistics, and general "
            "game rules."
        ),
    },
    {
        "name": "misc",
        "label": (
            "Minecraft topics that do not fit into the other categories, "
            "including versions, history, development, and other "
            "miscellaneous topics"
        ),
        "description": (
            "Questions about Minecraft topics that do not fit into the "
            "other categories, including versions, history, development, "
            "and other miscellaneous topics."
        ),
    },
]


def get_category_names() -> list[str]:
    """Retorna una lista con los nombres de todas las categorías."""
    return [category["name"] for category in CATEGORIES]


def get_category_labels() -> list[str]:
    """Retorna una lista con los labels legibles de todas las categorías."""
    return [category["label"] for category in CATEGORIES]


def get_category_descriptions() -> list[str]:
    """Retorna una lista con las descripciones de todas las categorías."""
    return [category["description"] for category in CATEGORIES]


def find_category_by_name(name: str) -> dict[str, str] | None:
    """Busca y retorna una categoría por su nombre. Retorna None si no existe."""
    for category in CATEGORIES:
        if category["name"] == name:
            return category

    return None