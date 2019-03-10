from django.contrib import admin

from .models import  ASIC, PCB, TestResult, NoiseTestResult, Connection

admin.site.register(ASIC)
admin.site.register(PCB)
admin.site.register(TestResult)
admin.site.register(NoiseTestResult)
admin.site.register(Connection)
