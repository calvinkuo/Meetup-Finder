from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url="meetup_finder/")),
    path('meetup_finder/', include('meetup_finder.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
