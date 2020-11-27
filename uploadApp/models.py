from django.db import models
from django.contrib.auth.models import User
# Create your models here.

import os
from django.dispatch import receiver

class Video(models.Model):
    #name= models.CharField(max_length=500)
    user=models.ForeignKey(to=User,on_delete=models.CASCADE)
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")
    
    def __str__(self):
        return self.user.username + ": " + str(self.videofile)


@receiver(models.signals.post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.videofile:
        if os.path.isfile(instance.videofile.path):
            os.remove(instance.videofile.path)
    