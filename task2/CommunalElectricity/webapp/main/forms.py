from django.forms import (Form, EmailInput, PasswordInput, IntegerField,
                          TextInput, CharField, EmailField, ModelChoiceField, Select)
from django.template.context_processors import request

from .models import Meter, User

class LoginForm(Form):
    email = EmailField(max_length=30,
                       widget=EmailInput(attrs={
                           'id': 'email',
                           'class': 'form-control',
                           'placeholder': 'Електронна пошта',
                       }))
    password = CharField(max_length=20,
                         widget=PasswordInput(attrs={
                             'id': 'password',
                             'class': 'form-control',
                             'placeholder': 'Пароль',
                         }))

class RegistrationForm(Form):
    name = CharField(max_length=20,
                        widget=TextInput(attrs={
                             'id': 'name',
                             'class': 'form-control',
                             'placeholder': 'Ім\'я',
                         }))
    email = EmailField(max_length=30,
                      widget=EmailInput(attrs={
                          'id': 'email',
                          'class' : 'form-control',
                          'placeholder': 'Електронна пошта',
                      }))
    password = CharField(max_length=20,
                      widget=PasswordInput(attrs={
                          'id': 'password',
                          'class' : 'form-control',
                          'placeholder': 'Пароль',
                      }))

class AddForm(Form):
    number = IntegerField(widget=TextInput(attrs={
                         'id': 'meter-num',
                         'class': 'form-control',
                         'placeholder': 'Номер лічильника',
                     }))

class SendForm(Form):

    def __init__(self, email, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = User.objects.filter(email=email).first()
        meters = Meter.objects.filter(user=user)
        self.fields['choiceMeter'].queryset = meters
        if meters.count() == 1:
            self.fields['choiceMeter'].initial = meters.first()

    choiceMeter = ModelChoiceField(
        queryset=Meter.objects.none(),
        required=True,
        widget=Select(attrs={'class': 'form-control', 'id': 'choice-field'})
    )
    dayValue =  IntegerField(widget=TextInput(attrs={
                         'id': 'day-value',
                         'class': 'form-control',
                         'placeholder': 'День',
                     }))
    nightValue = IntegerField(widget=TextInput(attrs={
        'id': 'night-value',
        'class': 'form-control',
        'placeholder': 'Ніч',
    }))


