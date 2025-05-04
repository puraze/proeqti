from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)

        if user and not user.is_superuser:
            try:
                allowed_category = Category.objects.get(name='ხალხის აზრები')
                self.fields['category'].queryset = Category.objects.filter(id=allowed_category.id)
                self.fields['category'].initial = allowed_category
                self.fields['category'].disabled = True
            except Category.DoesNotExist:
                self.fields['category'].queryset = Category.objects.none()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']