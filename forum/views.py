from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, ForumUser


def index(request):
	"""Load main page."""

	context = {"all_posts": Post.objects.all()}

	return render(request, "forum/index.html", context=context)


def log_user_in(request):
	"""A view to authenticate users upon login."""

	username = request.POST["username"]
	password = request.POST["password"]

	if username and password:
		query = "SELECT * FROM users WHERE username = '%s' and password = '%s'" % (username, password)
		current_user = ForumUser.objects.raw(query)

		if current_user:
			current_user = current_user[0]
			request.session["username"] = current_user.username
			request.session["user_id"] = current_user.f_user_id
			return redirect(index)

	return HttpResponse("Authentication failed.")


def create_account(request):
	"""A view to create a new user account."""

	username = request.POST["username"]
	email = request.POST["email"]
	password = request.POST["password"]
	current_user = ForumUser.objects.filter(username=username)

	if not current_user:
		current_user = ForumUser(username=username, email=email, password=password)
		current_user.save()
		return redirect(index)

	else:
		return HttpResponse("Account exists - choose a different username.")


def make_post(request):
	"""A view to make a new post to the forum."""

	title = request.POST["title"]
	comment = request.POST["comment"]
	user = ForumUser.objects.filter(f_user_id=request.session["user_id"])[0]

	new_post = Post(post_title=title, post_text=comment, poster=user)
	new_post.save()

	return redirect(index)


def log_user_out(request):
	"""A view to log out users."""

	request.session.flush()

	return redirect(index)


def delete_post(request):
	"""A view to delete posts from DB."""

	p_id = request.POST["id"]
	current_post = Post.objects.filter(post_id=p_id)[0]
	current_user = ForumUser.objects.filter(f_user_id=request.session["user_id"])[0]

	if current_post.poster.f_user_id == current_user.f_user_id:
		current_post.delete()

	return redirect(index)














