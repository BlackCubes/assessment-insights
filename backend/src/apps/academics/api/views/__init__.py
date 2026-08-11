from .period_collection import PeriodListCreateView
from .period_detail import PeriodDetailView
from .student_period_enrollment_collection import StudentPeriodEnrollmentListCreateView
from .student_period_enrollment_detail import StudentPeriodEnrollmentDetailView
from .term_collection import TermListCreateView
from .term_detail import TermDetailView

__all__ = [
    "PeriodDetailView",
    "PeriodListCreateView",
    "StudentPeriodEnrollmentDetailView",
    "StudentPeriodEnrollmentListCreateView",
    "TermDetailView",
    "TermListCreateView",
]
