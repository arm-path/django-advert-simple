from django import forms
from .models import Gallery, Image


class GalleryForm(forms.ModelForm):
    """Форма создания и редактирования галереи"""
    class Meta:
        model = Gallery
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ImageForm(forms.ModelForm):
    """Форма создания и редактирования изображения"""

    class Meta:
        model = Image
        fields = ['title', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }
