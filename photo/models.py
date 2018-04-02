from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from tagging.fields import TagField


class Photo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_posts')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=False, null=False, default='photos/no_image.jpg')
    title = models.CharField(max_length=100, null=False, blank=False, default='Default Title')
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tag = TagField()

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def get_absolute_url(self):
        return reverse('photo:post_detail', kwargs={'pk': self.id})
