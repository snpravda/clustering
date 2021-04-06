from django.db import models
from django.dispatch import receiver
import os


# Create your models here.
class Csv(models.Model):
    csv = models.FileField(upload_to='')

    def save(self, *args, **kwargs):
        '''delete old objects if new created'''
        if len(Csv.objects.all()) > 0:
            for obj in Csv.objects.all():
                obj.delete()

        super(Csv, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        "deleting files"
        os.remove(self.csv.path)
        super(Csv, self).delete(*args, **kwargs)

    def __str__(self):
        return self.csv.__str__()


@receiver(models.signals.post_delete, sender=Csv, dispatch_uid='post_pre_delete_signal')
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Csv` object is deleted.
    """
    if instance.csv:
        if os.path.isfile(instance.csv.path):
            os.remove(instance.csv.path)
