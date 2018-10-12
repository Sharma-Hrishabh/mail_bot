
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from .import views

app_name='home'


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.home,name="home"),
    url(r'^accounts/',include('accounts.urls')),
    url(r'^campaign/',include('campaign.urls')),

]
