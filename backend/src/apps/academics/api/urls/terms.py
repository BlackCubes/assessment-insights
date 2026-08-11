from django.urls import path

from apps.academics.api.views import TermDetailView, TermListCreateView

app_name = "terms"

urlpatterns = [
    path("", TermListCreateView.as_view(), name="list-create"),
    path("<uuid:uuid>/", TermDetailView.as_view(), name="detail"),
    path("<int:semester>/", TermDetailView.as_view(), name="detail"),
]
