from django.db import models
from django.contrib.auth.models import AbstractUser


DEPT_CHOICES = (
    ('PWSLab DevOps Support', 'PWSLab DevOps Support'),
    ('iSupport', 'iSupport'),
)

CATEGORY_CHOICES = (
    ('NEW Project CI/CD Pipeline Setup', 'NEW Project CI/CD Pipeline Setup'),
    ('Update CI/CD Pipeline Configuration', 'Update CI/CD Pipeline Configuration'),
    ('DevSecOps Pipeline Setup', 'DevSecOps Pipeline Setup'),
    ('CI/CD pipeline failure', 'CI/CD pipeline failure'),
    ('Automated Deployment failure', 'Automated Deployment failure'),
    ('Docker and Containers', 'Docker and Containers'),
    ('Kubernetes Deployments (like EKS/GCP)', 'Kubernetes Deployments (like EKS/GCP)'),
    ('Git Source control', 'Git Source control'),
    ('PWSLab server not responding (502/503 errors)', 'PWSLab server not responding (502/503 errors)'),
)

PRIORITY_CHOICES = (
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
)


class User(AbstractUser):

    username = None
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name}"


class Ticket(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    department = models.CharField(max_length=200, choices=DEPT_CHOICES)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    
    url = models.CharField(max_length=200)
    
    subject = models.CharField(max_length=200)
    description = models.TextField()
    
    status = models.CharField(max_length=200, default='open')
    priority = models.CharField(max_length=200, choices=PRIORITY_CHOICES)

    def __str__(self):
        return f"{self.id}_{self.subject}"

    class Meta:
        ordering = ['-id']
