from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'asics', views.ASICViewSet)
router.register(r'pcbs', views.PCBViewSet)
router.register(r'test-results', views.TestResultViewSet)
router.register(r'logbook-entries', views.LogbookEntryViewSet)
router.register(r'connections', views.ConnectionViewSet)

urlpatterns = [
    path('larpix-testing-db/', include(router.urls), name='larpix-testing-db')
]
