from django import forms
from django.forms import ModelForm

from gallery_app.models import Gallery
from .models import Advert


class AdvertForm(ModelForm):
    """Форма создания, редактирования и удаления объялвения"""

    def __init__(self, user_gallery=None, *args, **kwargs):
        """Переопределение метода конструктора для получения списка только галереии пользователя системы"""
        super().__init__(*args, **kwargs)
        if not user_gallery: # Срабатывает при обновлении объявления
            user_gallery = self.instance.user
        self.fields['gallery'].queryset = Gallery.objects.filter(
            user=user_gallery)

    class Meta:
        model = Advert
        fields = ['title', 'text', 'telephone_number', 'email', 'gallery']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'telephone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'gallery': forms.Select(attrs={'class': 'form-control'})
        }
