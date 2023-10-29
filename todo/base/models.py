from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
  name = models.CharField(max_length=200)
  
  def __str__(self):
    return self.name

class Article(models.Model):
  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  name = models.CharField(max_length=200)
  topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
  description = models.TextField(null=True, blank=True)
  article = models.TextField(null=True, blank=True)
  updated = models.DateTimeField(auto_now = True)
  created = models.DateTimeField(auto_now_add = True)
  
  def __str__(self):
    return self.name
  
