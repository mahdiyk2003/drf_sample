from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
	def create_user(self, email, full_name,is_author, password):
		if not is_author:
			raise ValueError('user must have opinion of the user being author')

		if not email:
			raise ValueError('user must have email')

		if not full_name:
			raise ValueError('user must have full name')

		user = self.model(email=self.normalize_email(email), full_name=full_name)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, full_name, password):
		is_author=True
		user = self.create_user(email, full_name,is_author, password)
		user.is_admin = True
		user.is_superuser = True
		user.save(using=self._db)
		return user