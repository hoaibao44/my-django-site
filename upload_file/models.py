from django.db import models
from django.conf import settings

# Create your models here.
class Document(models.Model):
    
    description = models.CharField(max_length=255,blank=True)
    document = models.FileField(upload_to='documents/')

    def file_name(self):
        return self.document.name

    def __str__(self):
        return self.description