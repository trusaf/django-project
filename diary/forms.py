from django import forms
from .models import Diary

class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['diary_type', 'target_date', 'title', 'content', 'shared_users', 'family_group']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
        }