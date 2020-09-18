from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # ex: /polls/comments/
    path('comments/', views.get_comments, name='comments'),
    # ex: /polls/comments/list/
    path('comments/list/', views.CommentListView.as_view(), name='commentList'),
]