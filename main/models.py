from django.db import models
from django.contrib.auth import get_user_model


class CV(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    skills = models.TextField()
    projects = models.TextField()
    bio = models.TextField()
    contacts = models.TextField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"



class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    query_string = models.CharField(max_length=255, blank=True, null=True)
    remote_ip = models.GenericIPAddressField(blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} {self.method} {self.path}"
