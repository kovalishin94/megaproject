from django import forms
from .models import Employee
from userprofiles.models import Userprofile


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['department'].empty_label = ''
        self.fields['profile'].empty_label = ''

    profile = forms.ModelChoiceField(
        queryset=Userprofile.objects.filter(employee=None),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Employee
        fields = [
            'first_name',
            'last_name',
            'surname',
            'date_of_birth',
            'email',
            'photo',
            'department',
            'position',
            'agreement_date',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'onfocus': "(this.type='date')",
                'onblur': "(this.type='text')"
            }
            ),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'agreement_date': forms.DateInput(attrs={
                'class': 'form-control',
                'onfocus': "(this.type='date')",
                'onblur': "(this.type='text')"
            }
            ),
        }
