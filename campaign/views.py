from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect,reverse
from .models import Contacts
from django.contrib.auth.decorators import login_required
from . import forms
import logging
from django.contrib import messages
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



def send(request):
    return HttpResponse('sent')


def upcsv(request):
    return redirect('campaign:upload_csv')


def upload_csv(request):
	data = {}
	if "GET" == request.method:
		return render(request, "campaign/upload_csv.html", data)
    # if not GET, then proceed
	try:
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			messages.error(request,'File is not CSV type')
			return HttpResponseRedirect(reverse("campaign:upload_csv"))
        #if file is too large, return
		if csv_file.multiple_chunks():
			messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse("campaign:upload_csv"))

		file_data = csv_file.read().decode("utf-8")


		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		for line in lines:
			fields = line.split(",")
			data_dict = {}
			data_dict["name"] = fields[0]
			data_dict["email"] = fields[1]
			try:
				form = EventsForm(data_dict)
				if form.is_valid():
					form.save()
				else:
					logging.getLogger("error_logger").error(form.errors.as_json())
			except Exception as e:
				logging.getLogger("error_logger").error(repr(e))
				pass

	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
		messages.error(request,"Unable to upload file. "+repr(e))

	return HttpResponseRedirect(reverse("campaign:upload_csv"))
