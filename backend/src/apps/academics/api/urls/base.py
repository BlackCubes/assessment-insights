from django.urls import include, path

app_name = "academics"

urlpatterns = [
    path("enrollments/", include("apps.academics.api.urls.student_period_enrollments", namespace="enrollments")),
    path("periods/", include("apps.academics.api.urls.periods", namespace="periods")),
    path("terms/", include("apps.academics.api.urls.terms", namespace="terms")),
]
