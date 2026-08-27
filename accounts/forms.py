from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.FileInput(),
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': '例：はじめまして。よろしくお願いします。(300文字以内)', 
                'class': 'bio-input',
            }),
        }