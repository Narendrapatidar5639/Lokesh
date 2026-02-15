from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    # ImageField ko CharField/URLField mein badla kyunki hum URL save karenge
    image = models.CharField(max_length=500, blank=True, null=True) 
    categories = models.ManyToManyField(Category)
    design_type = models.CharField(max_length=50, choices=[('2D', '2D'), ('3D', '3D')])
    interior_or_exterior = models.CharField(max_length=50, choices=[('Interior', 'Interior'), ('Exterior', 'Exterior')])
    plot_size = models.CharField(max_length=50, blank=True, null=True)
    # models.py mein 'design_loc' field (already sahi hai, bas length check karlein)
    design_loc = models.CharField(max_length=200, blank=True, null=True)
    contact_number = models.CharField(max_length=20,default="+919109231207", blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    # Yahan bhi URL save hoga
    image = models.CharField(max_length=500)

    def __str__(self):
        return self.project.title

class Feedback(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    ROLE_CHOICES = (('admin', 'Admin'), ('user', 'User'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')