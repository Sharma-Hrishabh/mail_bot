from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from .import views

app_name='campaign'

urlpatterns=[
url(r'^$',views.campaign,name="create"),
url(r'^review/',views.review,name="review"),
url(r'^send/',views.send,name="send"),
url(r'^upcsv/',views.upcsv,name="upcsv"),
url(r'^upload/csv/$', views.upload_csv, name='upload_csv'),



]
