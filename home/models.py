from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Announcement(models.Model):
    header = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    content = RichTextField(blank=True, null=True)
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return str(self.header) + " " + str(self.date)
