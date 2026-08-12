# oneday_todo/forms.py

from django import forms
from .models import OneDayList, OneDayTask


class OneDayListForm(forms.ModelForm):
    class Meta:
        model = OneDayList
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '例：勉強'}),
        }


class OneDayTaskForm(forms.ModelForm):
    class Meta:
        model = OneDayTask
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'タスクを入力'}),
        }