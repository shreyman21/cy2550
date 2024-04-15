from django.db import models

class StudentUser(models.Model):
    username=models.CharField(max_length=300)
    password=models.CharField(max_length=300)
    logged_in=models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Admin(models.Model):
    username=models.CharField(max_length=300)
    password=models.CharField(max_length=300)
    def __str__(self):
        return self.username