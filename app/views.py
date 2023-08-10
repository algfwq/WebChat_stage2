from django.shortcuts import render
from django.http import FileResponse
import os
# Create your views here.

def logo_down(request):
    file = open(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/logo/logo.ico', 'rb')
    response = FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="logo.ico"'
    return response

def user_image_down(request,username):
    current_path = os.path.abspath(__file__)
    file = open(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".") + '/user_image/' + username + '.png', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="logo.png"'
    return response

def login(request):
    return render(request, 'login.html')
