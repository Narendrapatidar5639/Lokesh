from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    # main image (optional now)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    design_type = models.CharField(
        max_length=50,
        choices=[('2D', '2D'), ('3D', '3D')]
    )

    interior_or_exterior = models.CharField(
        max_length=50,
        choices=[('Interior', 'Interior'), ('Exterior', 'Exterior')]
    )

    plot_size = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='projects/')

    def __str__(self):
        return self.project.title


# feedback user only
class Feedback(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"

#login/signup 

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
