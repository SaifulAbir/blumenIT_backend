from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from stuff.models import Role

# Create your models here.
from ecommerce.models import AbstractTimeStamp


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


phone_regex = RegexValidator(regex='^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$',message='Invalid phone number')


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verified_email = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    phone = models.CharField(max_length=255, validators=[phone_regex], null=True, blank=True)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='add_role_in_user_role', blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        elif self.username:
            full_name = self.username
        else:
            full_name = self.email
        return full_name

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-is_active']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'


class CustomerProfile(AbstractTimeStamp):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(
        User, verbose_name="User", on_delete=models.PROTECT, related_name="user_customer_profile")
    phone = models.CharField(max_length=255, validators=[phone_regex],null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(_("Birthday"), null=True, blank=True)
    avatar = models.ImageField(upload_to='customerAvatar', blank=True, null=True)

    def __str__(self):
        return self.user.email

    def associated_user(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profile"
        db_table = 'customer_profiles'


class Subscription(AbstractTimeStamp):
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        db_table = 'subscriptions'


class OTPModel(AbstractTimeStamp):
    """OTPModel to save otp value
    Args:
        contact_number: CharField
        otp_number: IntegerField
        expired_time: DateTimeField

    """
    contact_number = models.CharField(_('Contact Number'), max_length=20, null=False, blank=False)
    otp_number = models.IntegerField(_('OTP Number'), null=False, blank=False)
    verified_phone = models.BooleanField(default=False)
    expired_time = models.DateTimeField(_('Expired Time'), null=False, blank=False)

    def __str__(self):
        return self.contact_number

    class Meta:
        verbose_name = "OTPModel"
        verbose_name_plural = "OTPModels"
        db_table = 'otp_models'
