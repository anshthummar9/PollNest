from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Poll, Choice, Community

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter community name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your community...',
                'rows': 3
            })
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter your poll question...'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter choice text...'
            })
        }

    def clean_choice_text(self):
        text = self.cleaned_data.get('choice_text', '')
        if not text or not text.strip():
            return ''
        return text.strip()