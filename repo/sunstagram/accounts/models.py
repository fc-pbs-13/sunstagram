from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser


class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, name, password):
        if not email:
            raise ValueError('Users must have an email address')
        elif not username:
            raise ValueError('Users must have an username')
        elif not name:
            raise ValueError('Users must have an name')

        user = self.model(email=self.normalize_email(email),
                          username=username,
                          name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password):
        user = self.create_user(email=self.normalize_email(email),
                                username=username,
                                name=name,
                                password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

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