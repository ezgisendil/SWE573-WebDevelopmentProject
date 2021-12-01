from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
# for profile picture, extend the default users model that django provides
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shortbio = models.TextField(null=True, verbose_name='shortbio')
    interests = models.TextField(null=True, verbose_name='interests')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    timecredit = models.PositiveIntegerField(default=5)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)

        if img.height>300 or img.width>300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
