from django.apps import apps
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.text import gettext_lazy as _
from django.urls import reverse_lazy


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email and not username:
            raise ValueError('The given email and username must be set')
        email = self.normalize_email(email)
        GlobaslUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobaslUserModel.normalize_username(username)
        extra_fields.setdefault('user_slug', slugify(username))
        user = self.model(email=email, username=username, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, username, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """ Model User  """
    username_validator = UnicodeUsernameValidator()

    email = models.EmailField(_('email'), max_length=71, unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True, validators=[username_validator])
    user_slug = models.SlugField(_('user slug'), max_length=150, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    image = models.ImageField(_('image'), upload_to='profiles/%Y/%m', blank=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    city = models.CharField(_('city'), max_length=250, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('data joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_information(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'image': self.image,
                'date_of_birth': self.date_of_birth, 'city': self.city}

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name and self.last_name else self.username

    def get_short_name(self):
        return self.first_name if self.first_name else self.username

    def email_user(self, subject, message, from_emai=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True


class User(AbstractUser):

    def get_absolute_url(self):
        return reverse_lazy('profile:detail', args=[self.user_slug])

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
