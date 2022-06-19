from django.contrib import admin
from django.urls import path, include
from . views import *

# from .views import PostListViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'post', PostListViewSet, basename='user')


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('search/', PostListSearch.as_view()),
    path('create/', PostCreateImage.as_view()),
]
# urlpatterns += router.urls