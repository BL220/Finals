from django import forms
from django.core.validators import RegexValidator
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Delivery Address'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number',
                'pattern': '[0-9]+',
                'inputmode': 'numeric',
            }),
        }
        validators = {
            'phone': [RegexValidator(r'^\d+$', 'Phone number must contain only digits.')],
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if not phone.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone
