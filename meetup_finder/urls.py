from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'meetup_finder'
urlpatterns = [
    # ex: /meetup_finder/
    path('', views.EventListView.as_view(), name='index'),
    # ex: /meetup_finder/5/
    path('<int:pk>/', views.get_event_details, name='detail'),
    # ex: /meetup_finder/5/results/
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /meetup_finder/5/vote/
    path('<int:event_id>/comment/', views.writeComment, name='comment'),
    path('<int:event_id>/vote/', views.vote, name='vote'),
    # ex: /meetup_finder/comments/
    path('registration/', views.get_events, name='events'),
    # ex: /meetup_finder/comments/list/
    # path('comments/list/', views.CommentListView.as_view(), name='commentList'),
    # path('account/logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('<int:pk>/delete/', views.event_delete, name='event_delete')
]