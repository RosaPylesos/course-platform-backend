from typing import Annotated, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    model_validator,
)


class StrictSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HeadingContent(StrictSchema):
    text: str = Field(min_length=1)
    level: int = Field(ge=1, le=6)


class TextRun(StrictSchema):
    content: str
    marks: list[Literal
        ["bold", "italic", "underline"]
    ] = Field(
        default_factory=list
    )


class TextContent(StrictSchema):
    runs: list[TextRun]


class ImageContent(StrictSchema):
    url: HttpUrl
    alt: str = Field(min_length=1)
    caption: str | None = None


class VideoContent(StrictSchema):
    url: HttpUrl
    caption: str | None = None


class CalloutContent(StrictSchema):
    variant: Literal["info", "warning", "quote"]
    text: str = Field(min_length=1)


class CodeContent(StrictSchema):
    language: str = Field(min_length=1)
    code: str


class HeadingBlock(StrictSchema):
    id: UUID
    type: Literal["heading"]
    content: HeadingContent


class TextBlock(StrictSchema):
    id: UUID
    type: Literal["text"]
    content: TextContent


class ImageBlock(StrictSchema):
    id: UUID
    type: Literal["image"]
    content: ImageContent


class VideoBlock(StrictSchema):
    id: UUID
    type: Literal["video"]
    content: VideoContent


class CalloutBlock(StrictSchema):
    id: UUID
    type: Literal["callout"]
    content: CalloutContent


class CodeBlock(StrictSchema):
    id: UUID
    type: Literal["code"]
    content: CodeContent


LessonBlock = Annotated[
    HeadingBlock
    | TextBlock
    | ImageBlock
    | VideoBlock
    | CalloutBlock
    | CodeBlock,
    Field(discriminator="type"),
]


class LessonContent(StrictSchema):
    version: Literal[1] = 1
    blocks: list[LessonBlock] = Field(
        default_factory=list
    )

    @model_validator(mode="after")
    def check_unique_block_ids(self) -> "LessonContent":
        block_ids = [block.id for block in self.blocks]

        if len(block_ids) != len(set(block_ids)):
            raise ValueError("Block IDs must be unique")

        return self