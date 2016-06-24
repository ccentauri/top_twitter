from django.shortcuts import render
from django.core.mail import mail_admins, send_mail
from django.template import RequestContext

from .models import App


def post_list(request):
    apps = App.objects.order_by('title')
    return render(request, 'blog/post_list.html', {'apps': apps}, RequestContext(request))


def post_page(request, post_id):
    app = App.objects.get(id=post_id)
    return render(request, 'blog/post_page.html', {'app': app}, RequestContext(request))


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        sender = request.POST.get('email', '')

        recipients = ['cup.cake@inbox.ru']

        # mail_admins(subject, message, fail_silently=True)
        send_mail(subject,
                  "Name: " + name + "\n" + "Email: " + sender + "\n" + message,
                  sender, recipients, fail_silently=True)

        return render(request, 'blog/contact.html', {'sent_successful': True}, RequestContext(request))

    return render(request, 'blog/contact.html', {'sent_successful': False}, RequestContext(request))
