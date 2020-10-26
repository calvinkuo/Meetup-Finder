from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="meetup_finder/index.html")),
    path('meetup_finder/', include('meetup_finder.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
