
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('usr.urls')),
    path('',include('birth.urls')),
    path('',include('marriage.urls')),
    path('',include('death.urls')),
]
