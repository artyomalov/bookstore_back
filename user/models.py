import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# позволяет переписать модель менеджера управляющего моделями БД??
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, full_name, password, date_of_birth, avatar=None):

        if not email:
            raise ValueError('Email must be set')
        if not password:
            raise ValueError('Password must be set')
        if not full_name:
            ('Name must be set')

        email = self.normalize_email(email)
        user = self.create_user(
            email=email,
            full_name=full_name,
            avatar=avatar,
            date_of_birth=date_of_birth
        )
        user.set_password(password)
        user.save(using=self._db)  # при использовании нескольких
        # баз данных в проекте, параметр using позволит указать в какую БД сохранять модель
        return user

    def create_staffuser(self, email, full_name, password, date_of_birth, avatar=None):
        user = self.create_user(
            email=email,
            password=password,
            full_name=full_name,
            avatar=avatar,
            date_of_birth=date_of_birth
        )
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, full_name, password, date_of_birth, avatar=None):
        user = self.create_user(
            email=email,
            password=password,
            full_name=full_name,
            avatar=avatar,
            date_of_birth=date_of_birth
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email_adress',
        max_length=255,
        unique=True
    )
    full_name = models.CharField(
        null=False,
        blank=False,
        verbose_name='full_name'
    )
    password = models.CharField(
        null=False,
        blank=False,
        verbose_name='password'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    date_of_birth = models.DateField(default=datetime.date(2000, 1, 1))

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'full_name', 'date_of_birth']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_email(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
