
from django.urls import path\

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_posts, name="following"),
    path("newPost", views.new_post, name="newPost"),
    path("profile/<int:id>", views.view_profile, name="viewProfile"),
    path("followUser/<int:id>", views.follow_user, name="followUser"),
    path("unfollowUser/<int:id>", views.unfollow_user, name="unfollowUser"),
    
    # API Routes
     path("editPost/<int:id>", views.editPost, name="editPost"),
     path("likePost/<int:id>", views.likePost, name="likePost"),
     path("profile/likePost/<int:id>", views.likePost, name="likePost"),
     
]

