from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from profiles.models import UserProfile


class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def create(self, **kwargs):
        """
        User Object 생성시 해당 User의 PK값으로 UserProfile도 생성
        """
        user = self.model(**kwargs)
        self._for_write = True
        user.set_password(user.password)
        user.save()
        UserProfile.objects.update_or_create(user_id=user.id)
        return user

    def create_user(self, email, username, password):
        user = self.model(email=self.normalize_email(email),
                          username=username)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email=self.normalize_email(email), username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=20, unique=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [username]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # for permission
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # for permission
    def has_module_perms(self, app_label):
        return True

    #이거 넣으면 admin 페이지에서 로그인 불가
    # def save(self, *args, **kwargs):
    #     self.set_password(self.password)
    #     super().save(*args, **kwargs)