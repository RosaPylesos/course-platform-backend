from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    AUTHOR  = "author"
    ADMIN   = "admin"

class CourseDifficulty(str, Enum):
    BEGINNER        =  "beginner"
    INTERMEDIATE    =  "intermediate"
    ADVANCED        =  "advanced"

class EnrollmentStatus(str, Enum):
    ACTIVE      = "active"
    COMPLETED   = "completed"
    CANCELLED   = "cancelled"

class CourseStatus(str, Enum):
    PUBLISHED   = "published"
    DRAFT       = "draft"
    ARCHIVED    = "archived"

class SortBy(str, Enum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"

class SortOrder(str, Enum):
    ASC   = "asc"
    DESC  = "desc"