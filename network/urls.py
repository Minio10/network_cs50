
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post",views.new_post,name = "new_post"),
    path("profile/<str:username>",views.profile,name = "profile"),
    path("handleFollow/<str:username>/<int:flag>",views.handleFollow, name = "handleFollow"),
    path("following",views.following,name ="following"),
    path("newPost",views.newPost,name = "newPost"),

    # API Routes
    path("edit_posts/<int:id>", views.edit_posts, name="edit_posts"),
    path("manage_likes/<int:id>", views.manage_likes, name="manage_likes"),



]
