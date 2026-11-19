from typing import Annotated, Literal

from pydantic import ConfigDict, BaseModel, EmailStr, Field

from app.models.enums import CourseDifficulty



class SeedSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")



class SeedAuthorReference(SeedSchema):
    name: str = Field(min_length=1)
    surname: str | None = None
    email: EmailStr

class SeedTopicReference(SeedSchema):
    name: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    children: list["SeedTopicReference"] = Field(
        default_factory=list
    )

class SeedTagReference(SeedSchema):
    name: str = Field(min_length=1)
    slug: str = Field(min_length=1)

class SeedTagCategoryReference(SeedSchema):
    name: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    tags: list[SeedTagReference] = Field(
        default_factory=list
    )

class SeedReferenceData(SeedSchema):
    authors: list[SeedAuthorReference] = Field(
        min_length=1
    )
    topics: list[SeedTopicReference] = Field(
        min_length=1
    )
    tag_categories: list[SeedTagCategoryReference] = Field(
        min_length=1
    )



class SeedHeadingContent(SeedSchema):
    text: str = Field(min_length=1)
    level: int = Field(ge=1, le=6)

class SeedTextRun(SeedSchema):
    content: str
    marks: list[Literal
        ["bold", "italic", "underline"]
    ] = Field(
        default_factory=list
    )

class SeedTextContent(SeedSchema):
    runs: list[SeedTextRun] = Field(min_length=1)

class SeedImageContent(SeedSchema):
    alt: str = Field(min_length=1)
    caption: str | None = None

class SeedVideoContent(SeedSchema):
    caption: str | None = None

class SeedCalloutContent(SeedSchema):
    variant: Literal["info", "warning", "quote"]
    text: str = Field(min_length=1)

class SeedCodeContent(SeedSchema):
    language: str = Field(min_length=1)
    code: str



class SeedHeadingBlock(SeedSchema):
    type: Literal["heading"]
    content: SeedHeadingContent

class SeedTextBlock(SeedSchema):
    type: Literal["text"]
    content: SeedTextContent

class SeedImageBlock(SeedSchema):
    type: Literal["image"]
    content: SeedImageContent

class SeedVideoBlock(SeedSchema):
    type: Literal["video"]
    content: SeedVideoContent

class SeedCalloutBlock(SeedSchema):
    type: Literal["callout"]
    content: SeedCalloutContent

class SeedCodeBlock(SeedSchema):
    type: Literal["code"]
    content: SeedCodeContent



SeedBlock = Annotated[
    SeedHeadingBlock
    | SeedTextBlock
    | SeedImageBlock
    | SeedVideoBlock
    | SeedCalloutBlock
    | SeedCodeBlock,
    Field(discriminator="type")
]

class SeedLessonContent(SeedSchema):
    blocks: list[SeedBlock] = Field(min_length=1)



class SeedLesson(SeedSchema):
    name: str = Field(
        min_length=1,
        max_length=64,
    )
    description: str | None = None
    content: SeedLessonContent

class SeedCourse(SeedSchema):
    author_email: EmailStr
    topic_slug: str = Field(min_length=1)
    name: str = Field(
        min_length=1,
        max_length=64,
    )
    description: str | None = None
    difficulty: CourseDifficulty
    tag_slugs: list[str] = Field(default_factory=list)
    lessons: list[SeedLesson] = Field(min_length=1)

class SeedData(SeedSchema):
    courses: list[SeedCourse] = Field(min_length=1)