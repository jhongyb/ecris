from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.shortcuts import redirect,render
def error(request,exception):
    return render(request,'<h1>ERROR</h1>',status=404)

urlpatterns=[
    path('BIRTH',views.upload_birth_xml,name='uploadbirthxml'),
    path('BIRTH/list',views.birthlist,name='birthlist'),
    path('BIRTH/logentry',views.birthlogentry,name='birthlogentry'),
    path('BIRTH/logupdate<pk>',views.birthlogupdate,name='birthlogupdate'),
    path('BIRTH/logupdelete<pk>',views.birthlogdelete,name='birthlogdelete'),
    path('BIRTH/form1a<int:pk>',views.form_1a,name='form1a'),
    path('BIRTH/form1alist',views.form1alist,name='form1alist'),
     path('BIRTH/form1adelete<int:pk>',views.form1adelete,name='form1adelete'),
    path('BIRTH/form1a_form/<pk>',views.form_1a_report,name='form_1a_report')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

