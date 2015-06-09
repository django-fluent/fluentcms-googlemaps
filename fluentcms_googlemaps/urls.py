from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^marker-detail/$', views.MarkerDetailView.as_view(), name='fluentcms-googlemaps-marker-detail'),
]
