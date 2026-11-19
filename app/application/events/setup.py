from app.application.events.dispatcher import EventDispatcher
from app.application.events.course_events import CourseCompleted
from app.application.events.handlers.course_completed import(
    handle_course_completed,
)



def create_event_dispatcher() -> EventDispatcher:
    dispatcher = EventDispatcher()
    dispatcher.register(CourseCompleted, handle_course_completed)
    return dispatcher

event_dispatcher = create_event_dispatcher()