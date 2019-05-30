#userprofile models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    '''
    Helps Django work with our custom user model.
    '''
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_email_verified', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_email_verified', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    '''
    This a replaced user profile instead of the default django one
    '''
    gender_choices=[('M','Male'),('F','Female')]

    username=models.CharField(max_length=128,unique=True)
    email=models.CharField(max_length=256,unique=True)
    first_name=models.CharField(max_length=128)
    last_name=models.CharField(max_length=128)
    gender=models.CharField(max_length=1,choices=gender_choices,blank=True)
    joined_at=models.DateField(auto_now_add=True,blank=False)
    is_superuser=models.BooleanField()
    is_active=models.BooleanField()
    is_email_verified=models.BooleanField()
    is_staff=models.BooleanField()

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name']

    def get_full_name(self):
        '''
        Used to get users full name.
        '''
        return '{0} {1}'.format(self.first_name,self.last_name)

    def __str__(self):
        '''
        Django uses this when it needs to convert the object to a string.
        '''
        return self.username
