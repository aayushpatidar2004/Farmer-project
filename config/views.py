import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages

from .forms import ContactForm

logger = logging.getLogger(__name__)


def home(request):
    """Public homepage."""
    return render(request, 'home.html')


def about(request):
    """About page."""
    return render(request, 'about.html')


def contact(request):
    """Contact page and handler for public contact submissions."""
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.save()

            try:
                if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
                    send_mail(
                        subject=f"New contact form message: {contact_message.subject}",
                        message=(
                            f"Name: {contact_message.name}\n"
                            f"Email: {contact_message.email}\n\n"
                            f"Subject: {contact_message.subject}\n\n"
                            f"Message:\n{contact_message.message}\n"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.EMAIL_HOST_USER],
                        fail_silently=False,
                    )
            except Exception as exc:
                logger.exception('Failed to send contact form email: %s', exc)

            messages.success(request, 'Thank you for your message! Our team will contact you soon.')
            form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def error_403(request, exception):
    """Custom 403 access denied page."""
    return render(request, '403.html', {'message': str(exception) or 'Access denied.'}, status=403)


def error_404(request, exception):
    """Custom 404 error page."""
    return render(request, '404.html', status=404)


def error_500(request):
    """Custom 500 error page."""
    return render(request, '500.html', status=500)
