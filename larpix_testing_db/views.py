from django.views import View
from django.views.generic import CreateView, ListView
from rest_framework import viewsets
from .models import ASIC, PCB, TestResult, LogbookEntry, Connection
from .serializers import ASICSerializer, PCBSerializer, TestResultSerializer, LogbookEntrySerializer, ConnectionSerializer

class ASICViewSet(viewsets.ModelViewSet):
    queryset = ASIC.objects.all().order_by('-modification_date')
    serializer_class = ASICSerializer

class PCBViewSet(viewsets.ModelViewSet):
    queryset = PCB.objects.all().order_by('-modification_date')
    serializer_class = PCBSerializer

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all().order_by('-modification_date')
    serializer_class = TestResultSerializer

class LogbookEntryViewSet(viewsets.ModelViewSet):
    queryset = LogbookEntry.objects.all().order_by('-modification_date')
    serializer_class = LogbookEntrySerializer

class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all().order_by('-modification_date')
    serializer_class = ConnectionSerializer
