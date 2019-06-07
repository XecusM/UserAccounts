#userprofile models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    '''
    Helps Django work with our custom user model.
    '''
    # Create all data n migration
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        # Check if email is exists
        if not email:
            raise ValueError('User must have an email address')
        # normalize email for capital letters
        email = self.normalize_email(email)
        # variable for user model
        user = self.model(username=username, email=email, **extra_fields)
        # set user password
        user.set_password(password)
        # save user data
        user.save(using=self._db)
        # return user data
        return user

    def create_user(self, username, email,
                    password=None, **extra_fields):
        '''
        Method for normal user data defaults
        '''
        # set default fields
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_email_verified', False)
        # give defaults data to create user
        return self._create_user(username, email,
                                password, **extra_fields)

    def create_superuser(self, username, email,
                        password, **extra_fields):
        '''
        Method for super user data defaults
        '''
        # set default fields
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_email_verified', True)
        # check if super user is true
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        # check if staff is true
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        # give defaults data to create user
        return self._create_user(username, email,
                                 password, **extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    '''
    This a replaced user profile instead of the default django one
    '''
    # Create model fields
    username=models.CharField(max_length=128,unique=True)
    email=models.CharField(max_length=256,unique=True)
    first_name=models.CharField(max_length=128)
    last_name=models.CharField(max_length=128)
    joined_at=models.DateField(auto_now_add=True,blank=False)
    is_superuser=models.BooleanField(default = False)
    is_active=models.BooleanField(default = False)
    is_email_verified=models.BooleanField(default = False)
    is_staff=models.BooleanField(default = False)

    # include UserManager with this class model
    objects = UserManager()

    # Choose the username field
    USERNAME_FIELD = 'username'
    # Choose the required fields
    REQUIRED_FIELDS = ['email','first_name','last_name']

    # give and empty variable for the old email
    original_email = None

    def __init__(self, *args, **kwargs):
        '''
        Get the initial values of the user class
        '''
        # Add the inital values to the user class
        super(User, self).__init__(*args, **kwargs)
        # add the current email on the separit variable
        self.original_email = self.email

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        '''
        Save or create user data
        '''
        # check if the email doesn't changed
        if self.email != self.original_email:
          self.is_email_verified = False
        # get the inital method data
        super(User, self).save(force_insert, force_update, *args, **kwargs)
        # add the new email insrad of the current one
        self.original_email = self.email

    def get_full_name(self):
        '''
        Used to get users full name.
        '''
        # return the user full name
        return '{0} {1}'.format(self.first_name,self.last_name)

    def __str__(self):
        '''
        Django uses this when it needs to convert the object to a string.
        '''
        # return the username as string presentation
        return self.username
