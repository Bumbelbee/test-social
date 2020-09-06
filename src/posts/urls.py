from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('all',posts_list,name='posts-list'),
    path('liked',like_unlike_post,name="like-unlike"),
    path('<pk>/delete',PostDeleteView.as_view(),name="post-delete"),
    path('<pk>/update',PostUpdateView.as_view(),name="post-update"),
]
