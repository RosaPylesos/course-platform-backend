from uuid import UUID

from app.application.enrollments.repository import EnrollmentRepository
from app.application.enrollments.views import (
    EnrollmentStatusGroup,
    MyEnrollmentsView,
)

from app.models.enums import EnrollmentStatus



class GetMyEnrollmentsQuery:
    def __init__(
        self,
        enrollment_repository: EnrollmentRepository,
    ) -> None:
        self.enrollment_repository = enrollment_repository

    def execute(self, user_id: UUID) -> MyEnrollmentsView:

        ### CHECK
        # Probably should be transfered to some function
        # that groups all of these in one place.
        items = (
            self.enrollment_repository.list_by_user_with_progress(user_id)
            )

        grouped_items = {
            status: []
            for status in EnrollmentStatus
        }

        for item in items:
            grouped_items[item.status].append(item)

        status_counts = {
            status: len(status_items)
            for status, status_items in grouped_items.items()
        }

        groups = [
            EnrollmentStatusGroup(
                status=status,
                count=len(status_items),
                items=status_items,
            )
            for status, status_items in grouped_items.items()
        ]

        return MyEnrollmentsView(
            status_counts=status_counts,
            groups=groups,
        )