from django.urls import path

from . import views

urlpatterns = [
    path('marker-detail/', views.MarkerDetailView.as_view(), name='fluentcms-googlemaps-marker-detail'),
]
