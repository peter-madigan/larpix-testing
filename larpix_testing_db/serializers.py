from rest_framework import serializers
from .models import ASIC, PCB, TestResult, LogbookEntry, Connection

class ASICSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ASIC
        fields = ['id', 'version', 'packaged', 'status', 'qrcode', 'connection', 'test_results', 'note', 'logbook_entries', 'entry_date', 'modification_date', 'url']
        read_only_fields = ['qrcode', 'entry_date', 'modification_date']

class PCBSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PCB
        fields = ['id', 'version', 'status', 'qrcode', 'connections', 'test_results', 'note', 'logbook_entries', 'entry_date', 'modification_date', 'url']
        read_only_fields = ['qrcode', 'entry_date', 'modification_date']

class TestResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id', 'version', 'status', 'asics', 'pcbs', 'log', 'note', 'entry_date', 'logbook_entries', 'modification_date', 'url']
        read_only_fields = ['id', 'qrcode', 'entry_date', 'modification_date']

class LogbookEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LogbookEntry
        fields = ['id', 'type', 'version', 'title', 'entry', 'associated_test_results', 'associated_asics', 'associated_pcbs', 'entry_date', 'modification_date', 'url']
        read_only_fields = ['id', 'qrcode', 'entry_date', 'modification_date']

class ConnectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Connection
        fields = ['id', 'position_id', 'pcb', 'asic', 'entry_date', 'modification_date', 'url']
        read_only_fields = ['id', 'qrcode', 'entry_date', 'modification_date']
