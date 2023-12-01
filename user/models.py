import os
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _


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
    """
    return path for saving model's image
    """
    img_name, img_ext = os.path.splitext(instance.avatar.name)
    user_email = instance.email
    undotted_email = str(user_email).replace('.', '')
    new_img_name = f'{undotted_email}_avatar{img_ext}'

    return f'user/avatars/{new_img_name}'


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
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
        upload_to=upload_to,
        blank=True,
        null=True,
        verbose_name='avatar'
    )
    is_active = models.BooleanField(default=True, verbose_name='active')
    is_staff = models.BooleanField(default=False, verbose_name='staff')
    is_admin = models.BooleanField(default=False, verbose_name='admin')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', ]

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    # def get_email(self):
    #     return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        # if (
        #         self.avatar.name is not None and
        #         self.avatar.name != '/user/avatars/default_avatar.svg'
        # ):
        #
        #     super().save(*args, **kwargs)
        #     return
        super().save(*args, **kwargs)

    @property
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return 'media/user/avatars/default_avatar.svg'
