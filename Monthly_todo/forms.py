from django import forms
from .models import MonthlyList, MonthlyTask


class MonthlyListForm(forms.ModelForm):
    class Meta:
        model = MonthlyList
        fields = ['title', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '例：IELTS 7.0達成'}),
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class MonthlyTaskForm(forms.ModelForm):
    class Meta:
        model = MonthlyTask
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'タスクを入力'}),
        }