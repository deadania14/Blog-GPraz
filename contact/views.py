from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from random import randint
import gpraz.secrets as secret
from .models import VisitorMessage

# Create your views here.
def contact(request):
    request.session['current_page'] = 'contact'
    if request.method == 'POST':
        # Validate captcha
        c1 = int(request.POST.get('c1'))
        c2 = int(request.POST.get('c2'))
        captcha_user_response = int(request.POST.get('captcha-user-response'))
        if captcha_user_response == c1 + c2:
            visitor_name = request.POST.get('name')
            visitor_email = request.POST.get('email')
            visitor_message = request.POST.get('message')
            # Save visitor message to database
            vm = VisitorMessage(name=visitor_name, email=visitor_email, message=visitor_message)
            vm.save()
            # Send email to me
            send_mail(
                'GPraz - Message from %s' % visitor_name,
                'Sender email: %s\n\n%s' % (visitor_email, visitor_message),
                'GPraz <%s>' % secret.EMAIL_HOST_USER,
                [secret.DEFAULT_MAIL_RECIPIENT],
                fail_silently=False,
            )
            # Set flash message
            messages.info(request, 'Message sent successfully.')
        else:
            messages.error(request, "Security check failed. Are you... a robot?")
        return redirect('contact:contact')
    else:
        context = {
            'captcha1': randint(1, 20),
            'captcha2': randint(1, 20),
        }
        return render(request, 'contact/contact.html', context)
