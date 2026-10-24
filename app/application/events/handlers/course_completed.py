import logging

from app.application.events.course_events import CourseCompleted



logger = logging.getLogger(__name__)



def handle_course_completed(event: CourseCompleted) -> None:
    logger.info(
        "Course completed: user_id=%s, course_id=%s, enrollmentid=%s",
        event.user_id,
        event.course_id,
        event.enrollment_id,
    )