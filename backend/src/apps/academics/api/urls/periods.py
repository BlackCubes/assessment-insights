from django.urls import path

from api.views import PeriodListCreateView

urlpatterns = [path("", PeriodListCreateView.as_view(), name="period-collection")]
