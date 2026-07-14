from django.urls import include, path

app_name = "academics"

urlpatterns = [
    path("periods/", include("apps.academics.api.urls.periods", namespace="periods"))
]
