import datetime
import os
import sys
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _


# позволяет переписать модель менеджера управляющего моделями БД??


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, full_name=None, password=None, avatar=None):
        if not email:
            raise ValueError('Email must be set')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            avatar=avatar,
        )
        user.set_password(password)
        user.save(using=self._db)  # при использовании нескольких
        # баз данных в проекте, параметр using позволит указать в какую БД сохранять модель
        return user

    def create_staffuser(self, email, password, full_name=None, avatar=None):
        user = self.create_user(
            email=email,
            password=password,
            full_name=full_name,
            avatar=avatar,
        )
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, full_name=None, avatar=None):
        user = self.create_user(
            email=email,
            password=password,
            full_name=full_name,
            avatar=avatar,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user


def upload_to(instance, filename):
    return f'user/avatars/{instance}/{filename}'.format(filename=filename)


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email_adress',
        max_length=255,
        unique=True
    )
    full_name = models.CharField(
        blank=True,
        null=True,
        verbose_name='full_name'
    )
    password = models.CharField(
        verbose_name='password'
    )
    avatar = models.ImageField(
        _("Image"),
        default='media/user/avatars/default_avatar.svg',
        upload_to=upload_to,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', ]

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_email(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
