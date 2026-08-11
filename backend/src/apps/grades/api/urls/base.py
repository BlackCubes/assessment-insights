from django.urls import include, path

app_name = "grades"

urlpatterns = [path("", include("apps.grades.api.urls.student_grade_snapshots"))]
