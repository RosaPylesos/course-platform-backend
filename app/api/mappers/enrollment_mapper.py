from app.application.enrollments.views import(
    MyEnrollmentsView,
)

from app.schemas.enrollment import (
    MyEnrollmentsResponse,
    EnrollmentStatusGroupResponse,
    MyEnrollmentItemResponse,
    EnrollmentCourseSummaryResponse,
    EnrollmentProgressSummaryResponse,
)



def to_my_enrollments_response(
    view: MyEnrollmentsView,
) -> MyEnrollmentsResponse:

    return MyEnrollmentsResponse(
        status_counts=view.status_counts,
        groups=[
            EnrollmentStatusGroupResponse(
                status=group.status,
                count=group.count,
                items=[
                    MyEnrollmentItemResponse(
                        id=item.id,
                        created_at=item.created_at,
                        course=EnrollmentCourseSummaryResponse(
                            id=item.course.id,
                            name=item.course.name,
                            thumbnail_path=item.course.thumbnail_path,
                            status=item.course.status
                        ),
                        progress=EnrollmentProgressSummaryResponse(
                            lessons_total=item.progress.lessons_total,
                            lessons_started=item.progress.lessons_started,
                            lessons_completed=item.progress.lessons_completed
                        ),
                    )
                    for item in group.items
                ],
            )
            for group in view.groups
        ],
    )