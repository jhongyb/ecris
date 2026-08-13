from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
        path('marriage/',views.marriagelist, name='marriagelist'),
        path('marriage/uploadxml',views.upload_marriage_xml, name='uploadmarriagexml'),
        path('marriage/LogBookEntry',views.marriagelogentry, name='marriagelogentry'),
        path('marriage/LogBook<pk>Update',views.marriagelogupdate, name='marriagelogupdate'),
        path('marriage/LogBook<pk>Delete',views.marriagelogdelete, name='marriagelogdelete'),

        path('marriage/form3alist',views.form3alist, name='form3alist'),
        path('marriage/form<pk>3a',views.form_3a, name='form3a'),
        path('marriage/form<pk>3a_report',views.form_3a_report, name='form3areport'),
        path('marriage/form<pk>3a_delete',views.form3adelete, name='form3adelete'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)