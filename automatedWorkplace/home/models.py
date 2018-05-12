from django.db import models
from django.utils import timezone


class TableAutomatedWorkstation(models.Model):
    name = models.TextField();
    about = models.TextField();
# Create your models here.

class TableDevice(models.Model):
    name = models.TextField();

class TableDeviceSerial(models.Model):
        serial = models.TextField();
        ip = models.CharField(max_length=50);
        mode = models.CharField(max_length=100);
        IdWorkstation = models.ForeignKey(TableAutomatedWorkstation,on_delete=models.CASCADE);
