from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

ROLES = (
    ('User', 'User'),
    ('Recruiter', 'Recruiter'),
    ('Admin', 'Admin'),
)


# User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, mobile_number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not mobile_number:
            raise ValueError("The Mobile Number field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Admin must have is_superuser=True.')

        return self.create_user(email, mobile_number, password, **extra_fields)
    
# User's Model
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=20, choices=ROLES, default='User')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False) # admin
    is_superuser = models.BooleanField(default=False) # a superuser
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
