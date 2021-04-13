from django import forms
from django import forms
from .models import UserFile
from django.contrib.auth.models import User


class FileForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['file']

class FileShareForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Your provided Email {email} doesn't exist.")
        return email

class FileRenameForm(forms.Form):
    new_name = forms.CharField(max_length=100, label="New Name")