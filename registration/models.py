import secrets
import uuid
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .utils import content_file_name, message_file_name, upload_to


class CustomUser(AbstractUser):
    """
    Default User class
    """
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(default="User", max_length=255)
    last_name = models.CharField(default="User", max_length=255)
    identification = models.CharField(max_length=255, unique=True)
    state_of_residence = models.CharField(default="", max_length=255)
    city_of_residence = models.CharField(default="", max_length=255)
    phone = models.CharField(max_length=255, unique=True)
    emergency_number = models.CharField(max_length=255, unique=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    otp = models.CharField(max_length=255, default=uuid.uuid4, editable=False)
    verified_otp = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def generate_otp(self):
        self.otp = str(secrets.SystemRandom().randint(1000, 10000))
        return self.otp


class RegistrationForm(models.Model):
    """
    Registration From Model
    """
    need_to_train = models.BooleanField(default=False)
    need_trial_game = models.BooleanField(default=False)
    need_dorm = models.BooleanField(default=False)
    user = models.ForeignKey(to=CustomUser, related_name="registered_user", on_delete=models.CASCADE)


class Province(models.Model):
    name = models.CharField(_("name"), max_length=255)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(default="City", max_length=255)
    province_id = models.ForeignKey(to=Province, related_name="province_id", on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now(), null=True, blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), null=True, blank=True)

    def __str__(self):
        return self.name


class ContactUs(models.Model):
    name = models.CharField(default="cu", max_length=255)
    email = models.EmailField(max_length=254)
    subject = models.CharField(default="Subject", max_length=255)
    text = models.TextField(default="Message")
    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())


class UserAddress(models.Model):
    title = models.CharField(default="Title", max_length=255)
    address = models.TextField()
    phone = models.CharField(default="Phone", max_length=255)
    postal_code = models.CharField(default="", max_length=255)
    user = models.ForeignKey(to=CustomUser, related_name="user", on_delete=models.CASCADE)
    province_id = models.ForeignKey(to=Province, related_name="province", on_delete=models.SET_NULL, null=True)
    city_id = models.ForeignKey(to=City, related_name="city", on_delete=models.SET_NULL, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class PasswordReset(models.Model):
    email = models.EmailField(max_length=254)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=datetime.now())


class Sponsor(models.Model):
    title = models.CharField(default="Title", max_length=255)
    image = models.FileField(upload_to=upload_to, null=True, blank=True)


class License(models.Model):
    license_id = models.CharField(max_length=255, unique=True)
    hwid = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    app = models.CharField(max_length=255, null=True, blank=True)