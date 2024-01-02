from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .forms import RegisterForm

# SMTP Libraries
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from _config.utils import account_activation_token

# Views for User Authentication
def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if not form.is_valid():
            print(form.errors)
        
        if form.is_valid():
            # Save User Data
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Authenticate User
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            authenticate(username=username, password=raw_password)

            # Send Verification Mail
            current_site = get_current_site(request)

            # Render email html/text
            message = render_to_string('common/email-body-text.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            html_message = render_to_string('common/email-body.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            mail_title = "Please Verify Your email Address"
            mail_to = user.email

            # Send mail
            status = send_mail(
                mail_title,
                message=message,
                from_email="noreply@healingmentor.co.kr",
                recipient_list=[mail_to],
                html_message=html_message
            )

            if (not status):
                user.delete()

            context = {'email': user.email}
            return render(request, 'common/email-sent.html', context)
    else:
        form = RegisterForm()
    
    context = { 'form': form }
    return render(request, 'common/signup.html', context)

def terms(request):
    return render(request, 'common/terms.html')

def verify(request, uidb64, token):
    try:
        print(urlsafe_base64_decode(uidb64))
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print(e)
        user = None
    
    print(f"user = {user}, account_checked = {account_activation_token.check_token(user, token)}")
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'common/verify-success.html')
    else:
        return render(request, 'common/verify-fail.html')

def profile(request, username):
    user = User.objects.get(username=username)
    context = {'user': user}
    return render(request, 'common/profile.html', context)


# Views for Downloading Media
def download(request, path):
    from _config.settings.base import MEDIA_ROOT
    import os
    
    file_path = os.path.join(MEDIA_ROOT, path)

    if os.path.exists(file_path):
        file_ext = os.path.splitext(file_path)[-1]

        with open(file_path, 'r', encoding='UTF-8') as file:
            response = HttpResponse(file.read())
            response['Content-Disposition'] = f'attachment; filename="download{file_ext}"'
            return response


# Views for Error Handling
def error400(request, exception):
    return render(request, 'error/400.html', {})

def error403(request, exception):
    return render(request, 'error/403.html', {})

def error404(request, exception):
    return render(request, 'error/404.html', {})

def error500(request):
    return render(request, 'error/500.html', {})

def error502(request):
    return render(request, 'error/502.html', {})

def error503(request):
    return render(request, 'error/503.html', {})