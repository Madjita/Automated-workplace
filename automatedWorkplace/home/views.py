from django.shortcuts import render, get_object_or_404
from .models import TableAutomatedWorkstation, TableDevice, TableDeviceSerial


# Create your views here.
def index(request):
    automatedWorkstation = TableAutomatedWorkstation.objects.all();

    return render(request, 'home/index.html', {'automatedWorkstation': automatedWorkstation})
