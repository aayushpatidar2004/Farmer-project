from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Message',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject / Query topic',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your message here...',
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if not email:
            raise forms.ValidationError('Please enter your email address.')
        return email
