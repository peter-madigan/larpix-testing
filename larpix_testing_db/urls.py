from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'asic', views.ASICViewSet)
router.register(r'pcb', views.PCBViewSet)
router.register(r'test_result', views.TestResultViewSet)
router.register(r'logbook_entry', views.LogbookEntryViewSet)
router.register(r'connection', views.ConnectionViewSet)

urlpatterns = [
    path('larpix_testing_db/', include(router.urls))
]
