from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.log_user_in, name="login"),
	path("create-account", views.create_account, name="create-account"),
	path("create-post", views.make_post, name="create-post"),
	path("logout", views.log_user_out, name="logout"),
	path("delete-post", views.delete_post, name="delete-post")
	]