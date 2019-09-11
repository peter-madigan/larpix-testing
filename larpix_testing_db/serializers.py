from rest_framework import serializers
from .models import ASIC, PCB, TestResult, LogbookEntry, Connection

class ASICSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ASIC
        fields = ['pk', 'version', 'packaged', 'status', 'qrcode', 'note', 'entry_date', 'modification_date']
        read_only_fields = ['pk', 'qrcode', 'entry_date', 'modification_date']

class PCBSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PCB
        fields = ['pk', 'version', 'status', 'qrcode', 'note', 'entry_date', 'modification_date']
        read_only_fields = ['pk', 'qrcode', 'entry_date', 'modification_date']

class TestResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestResult
        fields = ['pk', 'version', 'status', 'asics', 'pcbs', 'log', 'note', 'entry_date', 'modification_date']
        read_only_fields = ['pk', 'qrcode', 'entry_date', 'modification_date']

class LogbookEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LogbookEntry
        fields = ['pk', 'type', 'version', 'title', 'entry', 'associated_test_results', 'associated_asics', 'associated_pcbs', 'entry_date', 'modification_date']
        read_only_fields = ['pk', 'qrcode', 'entry_date', 'modification_date']

class ConnectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Connection
        fields = ['pk', 'position_id', 'pcb', 'asic', 'entry_date', 'modification_date']
        read_only_fields = ['pk', 'qrcode', 'entry_date', 'modification_date']
