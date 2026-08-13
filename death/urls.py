from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns=[
    path('death/',views.deathlist,name='deathlist'),
    path('death/uploadXml',views.upload_death_xml,name='uploaddeathxml'),
    path('death/Death<pk>Remove',views.deathlogdelete,name='deathlogdelete'),
    path('death/Death<pk>Update',views.deathlogupdate,name='deathlogupdate'),
    path('death/DeathNewlog',views.deathlogentry,name='deathlogentry'),
    path('death/Deathform2alist',views.form2alist,name='form2alist'),
    path('death/Deathform<pk>2a',views.form_2a,name='form2a'),
    path('death/Deathform/<pk>/form2a',views.form_2a_report,name='form2areport'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)