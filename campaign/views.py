from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect,reverse
from .models import Contacts
from django.contrib.auth.decorators import login_required
from . import forms
import logging
from django.contrib import messages
import smtplib
import time
app_name='campaign'


@login_required(login_url="/accounts/login/")
def campaign(request):
    if request.method=='POST':
        form=forms.CreateContacts(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()            #save it
            return redirect('campaign:send')

    else:
        form = forms.CreateContacts()
    return render(request,'campaign/campaign.html',{'form':form})



# def send(request):
#     return HttpResponse('sent')


def upcsv(request):
    return redirect('campaign:upload_csv')

def upload_csv(request):
    data={}
    if "GET" == request.method:
        return render(request,"campaign/upload_csv.html",data)
    else:
        csv_file=request.FILES["csv_file"]
        file_data=csv_file.read().decode("utf-8")
        lines=file_data.split("\n")
        for line in lines:
            fields=line.split(",")
            print("sdfcsd"+fields[0])
            print("sdcdv"+fields[1])
            data_dict = dict()
            data_dict["name"]=fields[0]
            data_dict["email"]=fields[1]
            form=forms.CreateContacts(data_dict)
            if form.is_valid():
                form.save()
            else:
                print("error")
    return HttpResponseRedirect(reverse("campaign:review"))

def review(request):
    return render(request,"campaign/review.html")


def delcontacts(request):
    print("hello")
    Contacts.objects.all().delete()
    print("deleted")
    return HttpResponseRedirect(reverse("campaign:upload_csv"))

def send(request):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("man11invisible", "12345@@@@@")

    contacts=Contacts.objects.all()

    for contact in contacts:
        name=contact.name
        email=contact.email
        server.sendmail(
          "sharmahrishabh@cevgroup.org",
          email,
          "Hello! "+name+" keep up with you good work.")
        print(str(email),"\n")
        time.sleep(60)
    server.quit()

    return render(request,"campaign/successful.html")


def restart(request):
    return HttpResponseRedirect(reverse("campaign:create"))
