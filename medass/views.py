from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile

from _config.utils import uuid_filepath
from .models import MedassData

#@login_required(login_url='common:login')
def medass(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = MedassData()

            # Write user and time
            data.username = request.user
            data.date_created = timezone.now()

            # Write CSV data
            text_data = request.POST['csv_input']
            file_path = uuid_filepath(data, 'result.csv')
            data.csv_data.save(file_path, ContentFile(text_data))
            
            # Save into model
            data.save()

    return render(request, 'medass/medass.html')