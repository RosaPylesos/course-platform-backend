from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.models.topic import Topic
from app.models.course import Course

from app.schemas.topic import TopicCreate, TopicResponse, TopicUpdate

from app.utils.slug import generate_slug

router = APIRouter(
    prefix="/topics",
    tags=["Topics"],
)

@router.get("/", response_model=list[TopicResponse])
def get_topics(
    db: Session = Depends(get_db),
):
    statement = select(Topic).order_by(Topic.name)

    topics = db.scalars(statement).all()

    return topics

@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
):
    statement = select(Topic).where(
        Topic.id == topic_id
    )

    topic = db.scalar(statement)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    return topic

@router.post("/", response_model=TopicResponse, status_code=201)
def create_topic(
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
):

    slug = generate_slug(topic_data.name)

    base_slug = slug
    counter = 2

    while db.scalar(
        select(Topic.id).where(
            Topic.slug == slug
        )
    ) is not None:
        slug = f"{base_slug}-{counter}"
        counter+=1
    
    topic = Topic(
        name=topic_data.name,
        parent_id = topic_data.parent_id,
        slug=slug,
    )

    db.add(topic)
    db.commit()
    db.refresh(topic)

    return topic

@router.patch("/{topic_id}", response_model=TopicResponse)
def update_topic(
    topic_id: UUID,
    topic_data: TopicUpdate,
    db: Session = Depends(get_db)
):
    topic = db.get(Topic, topic_id)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    update_data = topic_data.model_dump(exclude_unset=True)

    if "name" in update_data:
        new_name = update_data["name"]

        if new_name is None:
            raise HTTPException(
                status_code=422,
                detail="Topic name cannot be null",
            )

        slug = generate_slug(new_name)
        base_slug = slug
        counter = 2

        while db.scalar(
            select(Topic.id).where(
                Topic.slug == slug,
                Topic.id != topic_id,
            )
        ) is not None:
            slug = f"{base_slug}-{counter}"
            counter+=1

        topic.name = new_name
        topic.slug = slug

        update_data.pop("name")

    for field, value in update_data.items():
        setattr(topic, field, value)

    db.commit()
    db.refresh(topic)

    return topic

@router.delete("/{topic_id}", status_code=204)
def delete_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
):
    topic = db.get(Topic, topic_id)

    if topic is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found",
        )

    has_children = db.scalar(
        select(Topic.id)
        .where(Topic.parent_id == topic_id)
        .limit(1)
    )

    if has_children is not None:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a topic that has child topics",
        )

    has_courses = db.scalar(
        select(Course.id)
        .where(Course.topic_id == topic_id)
        .limit(1)
    )

    if has_courses is not None:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a topic that has courses",
        )

    db.delete(topic)
    db.commit()