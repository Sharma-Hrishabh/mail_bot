from django.http import HttpResponse
from django.shortcuts import render

app_name='main'

def home(request):
    return render(request,'base_layout.html')
    #return HttpResponse('Hello')
