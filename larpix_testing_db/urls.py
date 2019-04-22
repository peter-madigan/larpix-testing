from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('asic/list', views.ASICListView.as_view(), name='ASICListView'),
    path('asic/create', views.ASICCreateView.as_view(), name='ASICCreateView')
]
