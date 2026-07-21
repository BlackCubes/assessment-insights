from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("academics/", include("apps.academics.api.urls", namespace="academics")),
    path("students/", include("apps.students.api.urls", namespace="students")),
]
