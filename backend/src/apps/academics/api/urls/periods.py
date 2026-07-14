from django.urls import path

from apps.academics.api.views import PeriodListCreateView

urlpatterns = [path("", PeriodListCreateView.as_view(), name="period-collection")]
