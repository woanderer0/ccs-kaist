from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile

from _config.utils import uuid_filepath
from .models import MedassData

#@login_required(login_url='common:login')
def medass_index(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = MedassData()

            # Write user and time
            data.user = request.user
            data.date_created = timezone.now()

            # Write CSV data
            from urllib.parse import unquote
            text_data = request.POST['csv_input']
            file_path = uuid_filepath(data, 'result.csv')
            data.csv_data.save(file_path, ContentFile(unquote(text_data)))
            
            # Save into model
            data.save()

    return render(request, 'medass/medass-index.html')

@login_required(login_url='common:login')
def medass_inquiry(request, username):
    user = User.objects.get(username=username)

    # Process inquiry only if user matches
    if request.user == user:
        # Initial variable settings    
        data_list = []
        csv_x_data_list = []
        csv_y_data_list = []

        # Fill data variable from raw database
        raw_data_list = MedassData.objects.filter(user=user)
        for data in raw_data_list:
            from _config.settings.base import MEDIA_ROOT
            from urllib.parse import quote
            import csv

            csv_x_data = []
            csv_y_data = []
            
            with open(f'{MEDIA_ROOT}/{data.csv_data}', 'r') as file:
                csv_data = csv.reader(file)
                for row in csv_data:
                    csv_x_data.append(float(row[0]))
                    csv_y_data.append(float(row[1]))

            csv_x_data_list.append(csv_x_data)
            csv_y_data_list.append(csv_y_data)

            data_list = zip(raw_data_list, csv_x_data_list, csv_y_data_list)

        # Send context to inquiry html template
        context = { 
            'data_list': data_list,
        }
        return render(request, 'medass/medass-inquiry.html', context)

    # Respond to (403)Forbidden if user does not match
    return HttpResponse(status=403)

@login_required(login_url='common:login')
def medass_delete(request, id):
    target_data = MedassData.objects.get(id=id)

    # Process delete only if user matches
    if target_data.user == request.user:
        target_data.delete()
        return redirect('medass:inquiry', request.user)

    # Respond to (403)Forbidden if user does not match
    return HttpResponse(status=403)