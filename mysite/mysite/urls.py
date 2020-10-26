from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('meetup_finder/', include('meetup_finder.urls')),
    path('admin/', admin.site.urls),
]
