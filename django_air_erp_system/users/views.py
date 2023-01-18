from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView
from airsite.models import Ticket
from django.db.models import Count
from django.utils import timezone


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'users/register.html', {'register_form': form})


class PersonalCabinetView(ListView):
     #context_object_name = 'flights'
    #template_name = 'users/personal_cabinet.html'

    def get_queryset(self):
        #flights =
        return Ticket.objects.filter(
            customer=self.request.user
        ).values('flight__name', 'flight__date').annotate(total=Count('id'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        upcoming_flights, previous_flights = [], []
        for flight in qs:

            if flight['flight__date'] > timezone.now():
                upcoming_flights.append(
                    (
                        flight['flight__name'], flight['flight__date'], flight['total'],
                        Ticket.objects.filter(
                            customer=self.request.user, flight__name=flight['flight__name'],
                            flight__date=flight['flight__date']).all()
                    )
                )
            elif flight['flight__date'] <= timezone.now():
                previous_flights.append(
                    (
                        flight['flight__name'], flight['flight__date'], flight['total'],
                        Ticket.objects.filter(
                            customer=self.request.user, flight__name=flight['flight__name'],
                            flight__date=flight['flight__date']).all()
                    )
                )

        context['upcoming_flights'] = upcoming_flights
        context['previous_flights'] = previous_flights
        return context









