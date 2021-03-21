from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from accounts.forms import AccountRegistrationForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib import messages
from accounts.models import Account

# Create your views here.


def register(request):
    form = AccountRegistrationForm()
    if request.method == 'POST':
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.is_active = False
            account.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('accounts/account_activation_email.html', {
                'account': account,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(account.pk)),
                'token': default_token_generator.make_token(account),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            # messages.info(
            #     request, 'Please confirm your email address to complete the registration!')
            return redirect('account_activation_confirm')
    else:
        form = AccountRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        account = get_user_model()._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        account = None
    if account is not None and default_token_generator.check_token(account, token):
        account.is_active = True
        account.save()
        return render(request, 'accounts/account_activation_complete.html')
    else:
        return render(request, 'accounts/account_activation_invalid.html')


def confirm_account(request):
    return render(request, 'accounts/account_activation_confirm.html')


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
