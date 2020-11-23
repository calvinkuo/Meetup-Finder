from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'meetup_finder'
urlpatterns = [
    path('', views.EventListView.as_view(), name='index'),

    path('<int:pk>/', views.event_details, name='detail'),
    path('new/', views.event_create, name='events'),
    path('<int:pk>/edit/', views.event_update, name='update'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('<int:pk>/add/', views.event_add, name='event_add'),
    path('<int:pk>/remove/', views.event_remove, name='event_remove'),

    path('<int:event_id>/comment/', views.write_comment, name='comment'),
    path('<int:event_id>/vote/', views.vote, name='vote'),

    path('profile/', views.profile, name='profile'),
    path('profile/remove/<int:pk>/', views.profile_event_remove, name='profile_event_remove'),
]