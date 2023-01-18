from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib import messages
from django.utils import dateformat
from django.urls import reverse
from urllib.parse import urlencode
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from datetime import datetime
from .forms import DestinationForm, UserForm
from .models import Flight, Ticket, Seat, Option
from .tasks import send_tickets_email
import random


class DestinationFormView(View):
    form_class = DestinationForm
    template_name = 'airsite/home.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        if form.is_valid():
            print(form.cleaned_data['from_city'])
            destination = str(form.cleaned_data['from_city']) + ' - ' + str(form.cleaned_data['to_city'])
            date = form.cleaned_data['date']
            passengers = form.cleaned_data['passengers']
            flights = Flight.objects.filter(name=destination).all()
            print(date)
            if flights:
                flight_date = [
                    flight.date for flight in flights if str(date) == str(dateformat.format(flight.date, 'Y-m-d'))
                ]
                try:
                    flight = Flight.objects.filter(name=destination, date=flight_date[0]).first()
                    if flight:
                        flight_passengers_count = flight.passengers - Ticket.objects.filter(
                            flight=flight.pk).all().count()
                        if passengers <= flight_passengers_count:
                            redirect_url = reverse('ticket-create')
                            query_string = urlencode({
                                'flight': flight.name, 'flight_datetime': flight.date, 'passengers': passengers
                            })

                            return redirect(f'{redirect_url}?{query_string}')
                        else:
                            messages.error(request, f"Sorry, but there are only {flight_passengers_count} seats left")
                    else:
                        messages.error(request,
                                       "Sorry, but there isn't a flight on that date, please try another date.")
                except IndexError:
                    messages.error(request, "Sorry, but there isn't a flight on that date, please try another date.")

            else:
                messages.error(request, f"Sorry, but there isn't a flight with that destination - {destination},"
                                        f" please try another destination.")
        return render(request, self.template_name, {'form': form})


class TicketCreateView(TemplateView):
    template_name = 'airsite/ticket_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        passengers = int(self.request.GET.get('passengers'))
        context['user_form'] = UserForm
        context['flight'] = self.request.GET.get('flight')
        context['flight_date'] = datetime.strptime(self.request.GET.get('flight_datetime'), "%Y-%m-%d %H:%M:%S.%f%z")
        context['passengers'] = self.request.GET.get('passengers')
        context['ticket_formset'] = modelformset_factory(Ticket, fields=('seat', 'option', 'option_2'), extra=passengers)
        return context

    def post(self, *args, **kwargs):
        data = self.request.POST
        context = self.get_context_data()
        formset = context['ticket_formset']
        data_for_formset = {k: v for k, v in data.items() if k not in ['first_name', 'last_name', 'email']}
        formset = formset(data=data_for_formset)
        if formset.is_valid():
            if not self.request.user.is_authenticated:
                form = UserForm(data={
                    k: v for k, v in data.items() if k in ['first_name', 'last_name', 'email', 'csrfmiddlewaretoken']
                })
                if form.is_valid():
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    email = form.cleaned_data['email']
                    if User.objects.filter(email=email).first().exists():
                        user = User.objects.filter(email=email).first()
                    else:
                        username = first_name + last_name + str(User.objects.all().last().pk + 1)
                        password = username + ''.join(map(str, random.sample(list(range(10)), k=3)))
                        User.objects.create_user(
                            username=username,
                            first_name=first_name, last_name=last_name, email=email, password=password
                            )
                        user = User.objects.filter(username=username).first()
                else:
                    messages.error(self.request, "Please, fill the user data correctly")
                    return self.render_to_response(context)
            else:
                user = self.request.user

            seat_list = [v for k, v in data_for_formset.items() if k.endswith('seat')]
            option_list = [v for k, v in data_for_formset.items() if k.endswith('option')]
            option2_list = [[v for k, v in data_for_formset.items() if k.endswith('option_2')]]

            flight = Flight.objects.filter(name=context['flight'], date=context['flight_date']).first()
            seats_and_options = list(zip(seat_list, option_list, option2_list))
            ticket_list = []
            for seat, option, option_2 in seats_and_options:
                seat_db = Seat.objects.get(pk=seat)
                if option:
                    option_db = Option.objects.get(pk=option)
                    ticket_price = flight.price + option_db.price
                    if option_2:
                        option_2_db = Option.objects.get(pk=option_2)
                        ticket_price += option_2_db.price
                else:
                    ticket_price = flight.price

                flight.booked_seats.add(seat)
                ticket_name = seat_db.name + context['flight'] + \
                              str(dateformat.format(context['flight_date'], 'Y-m-d H:M'))
                if option_db and not option_2_db:
                    t = Ticket.objects.create(
                        name=ticket_name, flight=flight, price=ticket_price,
                        customer=user, seat=seat_db, option=option_db
                    )
                elif option and option_2_db:
                    t = Ticket.objects.create(
                        name=ticket_name, flight=flight, price=ticket_price,
                        customer=user, seat=seat_db, option=option_db, option_2=option_2_db
                    )
                else:
                    t = Ticket.objects.create(
                        name=ticket_name, flight=flight, price=ticket_price,
                        customer=user, seat=seat_db
                    )

                ticket_list.append(t)

            send_tickets_email.delay(email, ticket_list)
            return redirect('ticket-success')
        else:
            messages.error(self.request, "Please, fill the tickets data correctly")

        return self.render_to_response(context)


class TicketSuccessView(TemplateView):
    template_name = 'airsite/ticket_success.html'













