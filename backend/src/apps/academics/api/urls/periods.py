from django.urls import path

from apps.academics.api.views import PeriodListCreateView

app_name = "periods"

urlpatterns = [path("", PeriodListCreateView.as_view(), name="list-create")]
