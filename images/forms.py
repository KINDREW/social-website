"""Model forms"""
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Image

class ImageCreateForm(forms.ModelForm):
    """Image creation form"""
    class Meta:
        """Pre described form"""
        model = Image
        fields = ("title","url","description")
        widgets = {"url":forms.HiddenInput,}

    def clean_url(self):
        """Checking the URL to see if valid"""
        url = self.cleaned_data["url"]
        valid_extentions= ["jpg", "jpeg"]
        extention = url.rsplit(".",1)[1].lower()
        if extention not in valid_extentions:
            raise forms.ValidationError("The given URL does not match \
                the vlaid image extentions.")
        return url

    def save(self, force_insert =False, force_update = False, commit = True):
        """Overiding the save method of ModelForms"""
        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image_url.rsplit(".",1)[1].lower()
        image_name = f"{name}.{extension}"
        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save = False)
        if commit:
            image.save()
        return image
