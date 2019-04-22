from django.contrib import admin

from .models import  ASIC, PCB, Connection, TestResult, LogbookEntry

admin.AdminSite.site_title = 'LArPix testing DB admin'
admin.AdminSite.site_header = 'LArPix testing DB'
admin.AdminSite.index_title = ''
admin.ModelAdmin.save_on_top = False
admin.ModelAdmin.show_full_result_count = True
admin.ModelAdmin.actions_on_top = False
admin.ModelAdmin.actions_on_bottom = True

class ConnectionInline(admin.TabularInline):
    model = Connection
    extra = 1
    fields = ['pcb', 'asic', 'position_id']
    autocomplete_fields = ['asic','pcb']

class TestResultsToASICInline(admin.TabularInline):
    model = TestResult.asics.through
    extra = 1
    verbose_name = 'Test Result'
    verbose_name_plural = 'Test results'
    autocomplete_fields = ['asic','testresult']

class TestResultsToPCBInline(admin.TabularInline):
    model = TestResult.pcbs.through
    extra = 1
    verbose_name = 'Test Result'
    verbose_name_plural = 'Test results'
    autocomplete_fields = ['pcb','testresult']

class ASICAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Chip information', { 'fields' : ['id', 'version', 'packaged', 'status', 'qrcode_tag', 'modification_date', 'entry_date', 'note']})
        ]
    inlines = [ConnectionInline, TestResultsToASICInline]
    list_display = ('id', 'version', 'packaged', 'status', 'entry_date', 'modification_date')
    list_display_links = ['id','version']
    list_editable = ['status']
    list_filter = ['version', 'packaged', 'status', 'modification_date', 'entry_date']
    search_fields = ['id','version','status','note']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'version', 'packaged', 'qrcode_tag', 'modification_date', 'entry_date']
        else:
            return ['id', 'qrcode_tag', 'modification_date', 'entry_date']

    def qrcode(self, obj):
        return generate_qrcode(obj)

class PCBAdmin(admin.ModelAdmin):
    fieldsets = [
        ('PCB information', { 'fields' : ['id', 'version', 'status', 'qrcode_tag', 'modification_date', 'entry_date', 'note']})
        ]
    inlines = [ConnectionInline, TestResultsToPCBInline]
    list_display = ('id', 'version', 'status', 'entry_date', 'modification_date')
    list_display_links = ['id','version']
    list_editable = ['status']
    list_filter = ['version', 'status', 'modification_date', 'entry_date']
    search_fields = ['id','version','status','note']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'version', 'qrcode_tag', 'modification_date', 'entry_date']
        else:
            return ['id', 'qrcode_tag', 'modification_date', 'entry_date']

class TestResultAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Test information', { 'fields' : ['version', 'id', 'status', 'log', 'pcbs', 'asics', 'note',]})
        ]
    list_display = ('id', 'version', 'status', 'entry_date', 'modification_date')
    list_display_links = ['id', 'version']
    list_editable = ['status']
    list_filter = ['version', 'status', 'modification_date', 'entry_date']
    search_fields = ['version','id','status','log','note']
    readonly_fields = ['id', 'modification_date', 'entry_date']

    filter_horizontal = ['pcbs','asics']

class LogbookEntryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Logbook entry', { 'fields' : ['title', 'type', 'id', 'modification_date', 'entry_date', 'entry', 'associated_pcbs', 'associated_asics', 'associated_test_results']})
        ]
    list_display = ('title', 'id', 'type', 'entry_date', 'modification_date')
    list_display_links = ['title','id']
    list_filter = ['type', 'modification_date', 'entry_date']
    search_fields = ['title','type','id','modification_date','entry_date','entry']
    readonly_fields = ['id','modification_date','entry_date']

    filter_vertical = ['associated_pcbs','associated_asics','associated_test_results']

admin.site.register(LogbookEntry, LogbookEntryAdmin)
admin.site.register(ASIC, ASICAdmin)
admin.site.register(PCB, PCBAdmin)
admin.site.register(TestResult, TestResultAdmin)
#admin.site.register(Connection)
