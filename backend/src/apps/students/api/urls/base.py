from django.urls import include, path

app_name = "students"

urlpatterns = [path("", include("apps.students.api.urls.students"))]
