from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'photo', 'telephone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'photo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'telephone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
