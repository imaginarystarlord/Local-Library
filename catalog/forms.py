import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RenewBookForm(forms.Form):
    renewable_date = forms.DateField(help_text='Enter A Date Between Today To 4 weeks (default 3)')

    def clean_renewable_date(self):
        data = self.cleaned_data['renewable_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date- renewable in past'))


        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid Date - renewable date 4 weeks ahead!'))

        return data

class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
