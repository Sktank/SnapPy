from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div
from django.contrib.auth import authenticate

__author__ = 'spencertank'

from django import forms
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
attrs_dict = {'class': 'required form-control'}


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username*"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("E-mail*"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password*"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)*"))

    def clean_username(self):
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean_password2(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'
        self.helper.layout = Layout(
            Div('username', css_class="form-group"),
            Div('password', css_class="form-group"),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            )
        )
        super(LoginForm, self).__init__(*args, **kwargs)

    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username*"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password*"))

    def clean_username(self):
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if not existing.exists():
            raise forms.ValidationError(_("That username does not exist"))
        else:
            return self.cleaned_data['username']

    def clean_password(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
            if user is None:
                raise forms.ValidationError(_("Incorrect Password."))
        return self.cleaned_data