from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

class Comments(models.Model):
    content = models.CharField(max_length=100)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, related_name='comments',on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author} for {self.post.title}'

    def get_absolute_url(self):
        return reverse('comment_detail', kwargs={'pk': self.pk})