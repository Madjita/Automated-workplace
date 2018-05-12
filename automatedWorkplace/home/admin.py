from django.contrib import admin
from .models import TableAutomatedWorkstation, TableDevice, TableDeviceSerial

admin.site.register(TableAutomatedWorkstation)
admin.site.register(TableDevice)
admin.site.register(TableDeviceSerial)
# Register your models here.
