from collections import defaultdict
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from datetime import date


# The following function will return the project Resource Pool for default value

def get_default_project():
    if Project.objects.filter(name = 'Resource Pool').exists():
        default_project = Project.objects.get(name = "Resource Pool")
    else:
        
        default_project = Project.objects.create(name = 'Resource Pool', start_date = '2021-08-13', end_date = '2022-08-13' )
        default_project.save()
    return default_project

# creating custom account manager for the resource model

class MyAccountManager(BaseUserManager):
    def create_user(self, name, email, password, experience):
        if not email:
            raise ValueError("Users must have an email")
        if not name:
            raise ValueError("Users must have a name")
        if not password:
            raise ValueError("Users must have a password")
        if not experience:
            raise ValueError("User's experience must be defined")
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            experience = experience,


        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, password, experience, name):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            experience = experience,
            name = name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

# Creating Project model that will hold information of projects present in the company

class Project(models.Model):
    
    name            =models.CharField(max_length=50)
    start_date      =models.DateField()
    end_date        =models.DateField()

    def __str__(self):
        return self.name


# Creating a custom user model 

class Resource(AbstractBaseUser):
    name            =models.CharField(max_length=50)
    email           =models.EmailField(verbose_name='email', max_length=60, unique=True)
    date_joined     =models.DateField(verbose_name='date_joined', auto_now_add=True)
    last_login      =models.DateField(verbose_name='last_login', auto_now=True)
    is_admin        =models.BooleanField(default=False)
    is_active       =models.BooleanField(default=True)
    is_staff        =models.BooleanField(default=False)
    is_superuser    =models.BooleanField(default=False)
    experience      =models.IntegerField()
    project         =models.ForeignKey(Project, on_delete=models.CASCADE, default=get_default_project())

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['experience', 'name']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# Creating Release model that will hold information of releases in a particular project

class Release(models.Model):
    project             = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='releases')
    release_date        = models.DateField()
    version             = models.FloatField()
    description         = models.CharField(max_length=1000)


