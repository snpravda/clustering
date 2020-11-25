from django.db import models
from django.dispatch import receiver
import os

# Create your models here.
class Csv(models.Model):
    csv = models.FileField(upload_to='')


    def __str__(self):
        return self.csv.__str__()


@receiver(models.signals.post_delete, sender=Csv, dispatch_uid='post_pre_delete_signal')
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Csv` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
