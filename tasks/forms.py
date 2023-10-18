from django import forms
from .models import Task


class TaskAddForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'deadline',
            'target_employee',
            'task_file',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'onfocus': "(this.type='date')",
                'onblur': "(this.type='text')"
            }
            ),
            'target_employee': forms.Select(attrs={'class': 'form-control'}),
            'task_file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class TaskAnswerForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'answer',
            'answer_file',
        ]
        widgets = {
            'answer': forms.Textarea(attrs={'class': 'form-control', 'required': ''}),
            'answer_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
