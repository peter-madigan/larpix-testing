from django.views import View
from django.views.generic import CreateView, ListView
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import ASIC, PCB, TestResult, LogbookEntry, Connection
from .serializers import ASICSerializer, PCBSerializer, TestResultSerializer, LogbookEntrySerializer, ConnectionSerializer

class ASICViewSet(viewsets.ModelViewSet):
    queryset = ASIC.objects.all()
    serializer_class = ASICSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'version', 'packaged', 'status', 'note', 'entry_date', 'modification_date']

class PCBViewSet(viewsets.ModelViewSet):
    queryset = PCB.objects.all()
    serializer_class = PCBSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'version', 'status', 'note', 'entry_date', 'modification_date']

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'version', 'status', 'log', 'note', 'entry_date', 'modification_date']

class LogbookEntryViewSet(viewsets.ModelViewSet):
    queryset = LogbookEntry.objects.all()
    serializer_class = LogbookEntrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'type', 'version', 'title', 'entry', 'entry_date', 'modification_date']

class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'position_id', 'entry_date', 'modification_date']
