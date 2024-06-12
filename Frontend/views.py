from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import os
from Frontend.Plugins import main

def index(request):
    return render(request,'Frontend/index.html')

def about(request):
    return render(request,'Frontend/about.html')

def team(request):
    return render(request,'Frontend/team.html')

def contact(request):
    return render(request,'Frontend/contact.html')

def login(request):
    return render(request,'Frontend/login.html')

def register(request):
    return render(request,'Frontend/register.html')

def listenToFrontend(request):
    if request.method == 'POST' and 'blob' in request.FILES:
        audio_file = request.FILES['blob']
        save_path = os.path.join(settings.MEDIA_ROOT, 'audio', 'temp.wav')
        with open(save_path, 'wb+') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        main.start()
        return JsonResponse({'message': 'Audio file received and saved successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


