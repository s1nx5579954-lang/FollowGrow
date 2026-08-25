from django import forms
from .models import MonthlyList


class MonthlyListForm(forms.ModelForm):
    class Meta:
        model = MonthlyList
        fields = ['title', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '例：IELTS 7.0達成'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
