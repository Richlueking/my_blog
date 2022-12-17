from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('bloglist/', views.blogList, name="bloglist"),

    path('blog/<str:pk>/', views.blog, name="blog"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-blog/', views.createBlog, name="create-blog"),
    path('update-blog/<str:pk>/', views.updateBlog, name="update-blog"),
    path('delete-blog/<str:pk>/', views.deleteBlog, name="delete-blog"),

    path('delete-comment/<str:pk>/', views.deleteComment, name="delete-comment"),

    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('like/<str:pk>/', views.LikeView, name='like_blog'),
]
