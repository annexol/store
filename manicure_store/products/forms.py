from django import forms

from .models import User


class OrderForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван'}),
                           max_length=50, required=True)
    number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '375297777777'}),
        max_length=12, required=True

    )
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'г. Минск, ул. Мира, дом 6',
    }), max_length=200, required=True)

    class Meta:
        model = User
        fields = ('name', 'number', 'address')
