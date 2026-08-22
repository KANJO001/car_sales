from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Car, CarImage, Profile


# ========================================== #
# CAR FORM WITH MULTIPLE IMAGES              #
# ========================================== #
class CarForm(forms.ModelForm):
    images = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Car Images (Select multiple)',
        help_text='Upload up to 10 images (JPEG, PNG, WebP, GIF)'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add 'multiple' attribute AFTER widget initialization
        self.fields['images'].widget.attrs['multiple'] = True

    class Meta:
        model = Car
        fields = [
            'make', 'model', 'year', 'price', 'mileage',
            'fuel_type', 'transmission', 'body_type',
            'description', 'is_available'
        ]
        widgets = {
            'make': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Toyota'
            }),
            'model': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Camry'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2024'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '25000'
            }),
            'mileage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '15000'
            }),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'body_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your car...'
            }),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'make': 'Make',
            'model': 'Model',
            'year': 'Year',
            'price': 'Price ($)',
            'mileage': 'Mileage (km)',
            'fuel_type': 'Fuel Type',
            'transmission': 'Transmission',
            'body_type': 'Body Type',
            'description': 'Description',
            'is_available': 'Available',
        }


# ========================================== #
# CAR EDIT FORM                              #
# ========================================== #
class CarEditForm(CarForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'].help_text = 'Upload additional images (max 10 total). Existing images are shown below.'


# ========================================== #
# USER UPDATE FORM                           #
# ========================================== #
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }


# ========================================== #
# PROFILE UPDATE FORM                        #
# ========================================== #
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'bio', 'profile_picture']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your Address'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ========================================== #
# CUSTOM REGISTRATION FORM                   #
# ========================================== #
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['password1'].validators = []
        self.fields['password2'].validators = []
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username',
            'autofocus': True
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'required': True
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })