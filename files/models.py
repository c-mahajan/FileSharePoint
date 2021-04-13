from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import datetime

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.uploader.id, filename)

class UserFile(models.Model):
    file_name = models.CharField(max_length=100)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    uploaded_on = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_with')
    size = models.CharField(max_length=10)
    in_trash = models.BooleanField(default=0, blank=False)
    file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(["pdf","jpg","jpeg","png","gif","doc","docx", "xls","xlsx","ppt","pptx","java","class","py","gif"])], blank=False)

    def __str__(self):
        return f"{self.id} - {self.file_name}"
