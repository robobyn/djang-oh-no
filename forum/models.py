from django.db import models
from django.conf import settings


class ForumUser(models.Model):
	"""A forum user who can leave comments on forum."""

	f_user_id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=30, blank=False,
		null=False, default=None)
	email = models.CharField(max_length=30, blank=False,
		null=False, default=None)
	password = models.CharField(max_length=20, blank=False,
		null=False, default=None)

	def __str__(self):

		return self.username

	class Meta:
		db_table = 'users'


class Post(models.Model):
	"""A post a user leaves on a forum."""

	post_id = models.AutoField(primary_key=True)
	post_text = models.CharField(max_length=500, blank=False,
		null=False, default=None)
	post_title = models.CharField(max_length=60, blank=False,
		null=False, default=None)
	poster = models.ForeignKey(ForumUser, on_delete=models.PROTECT, default=None)

	def __str__(self):

		return self.post_title

	class Meta:
		db_table = 'posts'
