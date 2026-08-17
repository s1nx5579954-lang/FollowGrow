from django import forms
from .models import DailyReflection


class DailyReflectionForm(forms.ModelForm):
    class Meta:
        model = DailyReflection
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'★{"★"*(i-1)}') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': '今日の振り返りを書いてみましょう'}),
        }