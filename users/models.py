from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    description = models.TextField(default='Hello, i am a new one here.')

    def __str__(self):
        return f'{self.user.username} Profile'