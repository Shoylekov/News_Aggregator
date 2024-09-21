from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    topics = models.CharField(max_length=255)  # Store user-preferred topics as a comma-separated string

    def __str__(self):
        return self.user.username
    
    
class SavedArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title