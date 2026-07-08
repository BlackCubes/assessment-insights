from django.urls import path

from .views import StudentDetailView, StudentListView

urlpatterns = [
    path("", StudentListView.as_view(), name="student-list"),
    path("<uuid:uuid>/", StudentDetailView.as_view(), name="student-detail"),
    path("<int:student_id>/", StudentDetailView.as_view(), name="student-detail"),
]
