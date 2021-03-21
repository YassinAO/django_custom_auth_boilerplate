from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _


class AccountRegistrationForm(UserCreationForm):
    """
    A Custom form for creating new users.
    """

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password1', 'password2']


class EmailValidationOnForgotPassword(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not get_user_model().objects.filter(email__iexact=email, is_active=True).exists():
            msg = _("There is no account registered with the specified email.")
            self.add_error('email', msg)
        return email
