from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone
from .models import Flight, Ticket
from users.models import Profile
from django.db.models import Count
import requests


@shared_task()
def send_tickets_email(email_address: str, info: list):
    message = 'Hello, there are your tickets:\n\n'
    for ticket in info:
        message += f'Ticket - {ticket.name}\n\n Flight - {ticket.flight.name}\n\n Price - {ticket.price}\n\n' \
                   f'Customer - {ticket.customer.first_name + ticket.customer.last_name}\n\n' \
                   f'Seat - {ticket.seat.name}\n\n'
        if ticket.option:
            message += f'First option - {ticket.option}\n\n'
        elif ticket.option_2:
            message += f'Second option - {ticket.option}\n\n'

    message += 'Thank you for using our service.\n Have a good fly!'
    send_mail(
        'Your tickets',
        message,
        'dimonchik5490@gmail.com',
        [email_address],
        fail_silently=True
    )


# Periodic task, that makes post request to mock flask url
# to notify users that have a flight tomorrow via webhook
@shared_task(name='django_air.tasks.webhook_notify')
def webhook_notify():
    # url = 'http://localhost:3000/webhook'
    current_date = timezone.now()
    users_to = Ticket.objects \
        .values('customer', 'flight') \
        .filter(flight_date__day=current_date.day + 1).annotate(total=Count('id'))
    for user in users_to:
        flight = Flight.objects.get(pk=user['flight'])
        url = Profile.objects.filter(user=user['customer']).url
        message = f"Don't forget, that you have tickets for flight - {flight.name}" \
                  f" tomorrow at {flight.date.hour}:{flight.date.minute}."
        requests.post(url, data={'notification': message})


