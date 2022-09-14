from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': "Nom d'utilisateur",
        'autofocus': True
    }), error_messages={'required': 'Please enter your name'})

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
        }
    ), error_messages={'required': 'Please enter your password'})


class EditProfilForm(forms.Form):
    nom = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'id': 'c-name',
            'class': 'form-control',
            'required': False
        }
    ))
    prenom = forms.CharField(max_length=100, widget=forms.TextInput(
            attrs={
                'id': 'c-prenom',
                'class': 'form-control',
                'required': False
            }
    ))

    email = forms.EmailField()
    email.widget.attrs.update(
        {
            'class': 'form-control',
        }
    )
    image = forms.FileField()

    image.widget.attrs.update(
        {
            'class': 'file-drop-input',
            'accept': '.png, .jpg, .jpeg',
        }
    )