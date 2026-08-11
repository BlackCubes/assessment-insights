from django.urls import path

from apps.academics.api.views import PeriodDetailView, PeriodListCreateView

app_name = "periods"

urlpatterns = [
    path("", PeriodListCreateView.as_view(), name="list-create"),
    path("<uuid:uuid>/", PeriodDetailView.as_view(), name="detail"),
    path("<int:period_number>/", PeriodDetailView.as_view(), name="detail"),
]
