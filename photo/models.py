from io import BytesIO

import os
from PIL import Image, ImageFilter
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse
from tagging.fields import TagField

from mysite.settings import BASE_DIR


class Photo(models.Model):
    fs = FileSystemStorage(location=os.path.join(BASE_DIR, 'media'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_posts')
    photo = models.ImageField(storage=fs, blank=False, default='photo/no_images.png')
    title = models.CharField(max_length=100, null=False, blank=False, default='Default Title')
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tag = TagField()

    mod_num = models.IntegerField(default=0)
    editted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.author.username + " " + self.created.strftime("%Y-%m-%d %H:%M:%S")

    def save(self, *args, **kwargs):
        # is_duplicated = False
        # print(bool(self.photo))
        if self.editted:
            pass
        elif self.created != self.updated:
            self.editted = True

        if self.mod_num == 0:
            if self.editted:
                before_obj = Photo.objects.get(id=self.id)
                if before_obj.photo != self.photo:
                    before_obj.photo.delete(save=False)

            super(Photo, self).save(*args, **kwargs)

        else:
            image_obj = Image.open(self.photo)
            image_obj = image_obj.convert('RGB')
            if self.mod_num == 1:
                image_obj = image_obj.convert('L')
            if self.mod_num == 2:
                image_obj = image_obj.filter(ImageFilter.BLUR)
            if self.mod_num == 3:
                image_obj = image_obj.filter(ImageFilter.CONTOUR)

            new_image_io = BytesIO()
            image_obj.save(new_image_io, format='JPEG')
            temp_name = self.photo.name

            if self.editted:
                before_obj = Photo.objects.get(id=self.id)
                before_obj.photo.delete(save=False)
                self.photo.save(temp_name, content=ContentFile(new_image_io.getvalue()), save=False)
                super(Photo, self).save(*args, **kwargs)
                return          
            
            self.photo.save(temp_name, content=ContentFile(
                new_image_io.getvalue()), save=False)
            super(Photo, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('photo:post_detail', kwargs={'pk': self.id})
