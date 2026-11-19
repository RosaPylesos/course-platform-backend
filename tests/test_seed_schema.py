from app.schemas.seed import SeedData


data = {
    "courses": [
        {
            "author_email": "author@example.com",
            "topic_slug": "python",
            "name": "Основы Python",
            "description": None,
            "difficulty": "beginner",
            "tag_slugs": ["python", "git"],
            "lessons": [
                {
                    "name": "Первый урок",
                    "description": None,
                    "content": {
                        "blocks": [
                            {
                                "type": "heading",
                                "content": {"text": "Введение", "level": 1},
                            },
                            {
                                "type": "text",
                                "content": {
                                    "runs": [
                                        {"content": "Привет!", "marks": ["bold"]}
                                    ]
                                },
                            },
                            {
                                "type": "image",
                                "content": {"alt": "Пример изображения"},
                            },
                            {
                                "type": "video",
                                "content": {},
                            },
                            {
                                "type": "callout",
                                "content": {
                                    "variant": "info",
                                    "text": "Полезная информация",
                                },
                            },
                            {
                                "type": "code",
                                "content": {
                                    "language": "python",
                                    "code": "print('Hello, world!')",
                                },
                            },
                        ]
                    },
                }
            ],
        }
    ]
}


seed_data = SeedData.model_validate(data)

print("Validation successful!")
print(seed_data.model_dump())

#####

from pydantic import ValidationError


def check_invalid_data(data: dict, description: str):
    try:
        SeedData.model_validate(data)
    except ValidationError:
        print(f"OK — rejected: {description}")
    else:
        raise AssertionError(f"Invalid data was accepted: {description}")


# Неизвестный тип блока
invalid_type = data.copy()
invalid_type["courses"] = [
    {
        **data["courses"][0],
        "lessons": [
            {
                **data["courses"][0]["lessons"][0],
                "content": {
                    "blocks": [{"type": "unknown", "content": {}}]
                },
            }
        ],
    }
]

check_invalid_data(invalid_type, "unknown block type")


# Пустой список блоков
empty_blocks = data.copy()
empty_blocks["courses"] = [
    {
        **data["courses"][0],
        "lessons": [
            {
                **data["courses"][0]["lessons"][0],
                "content": {"blocks": []},
            }
        ],
    }
]

check_invalid_data(empty_blocks, "empty blocks")


# Некорректная сложность
invalid_difficulty = data.copy()
invalid_difficulty["courses"] = [
    {**data["courses"][0], "difficulty": "expert"}
]

check_invalid_data(invalid_difficulty, "invalid difficulty")