from django.db import models

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    pw = models.CharField(max_length=50)
    name = models.CharField(max_length=50, default='None')

class PostModel(models.Model):
    post_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    author_id = models.CharField(max_length=50)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()