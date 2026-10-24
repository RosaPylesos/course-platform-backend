from uuid import uuid4

from app.application.events.course_events import CourseCompleted
from app.application.events.setup import create_event_dispatcher

import logging

logging.basicConfig(level=logging.INFO)

dispatcher = create_event_dispatcher()

event = CourseCompleted(
    enrollment_id=uuid4(),
    user_id=uuid4(),
    course_id=uuid4(),
)

dispatcher.dispatch(event)

print("Event dispatched successfully")
