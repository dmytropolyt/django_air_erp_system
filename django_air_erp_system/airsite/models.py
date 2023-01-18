from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class City(models.Model):
    name = models.CharField(max_length=50, unique=True, primary_key=True)

    def __str__(self):
        return f'{self.name}'


class Flight(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    airplane = models.CharField(max_length=20)
    passengers = models.IntegerField(default=150)
    booked_seats = models.ManyToManyField('Seat', blank=True)
    price = models.PositiveIntegerField(blank=True, default=20)

    def __str__(self):
        return f'{self.name}, {self.date}'


class Seat(models.Model):
    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f'{self.name}'


class Option(models.Model):
    name = models.CharField(max_length=10, unique=True)
    price = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f'{self.name}'


class Ticket(models.Model):
    name = models.CharField(max_length=40)
    flight = models.ForeignKey(Flight, related_name='ticket', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=40)
    customer = models.ForeignKey(User, related_name='ticket', on_delete=models.CASCADE)
    discount = models.IntegerField(default=0)
    seat = models.OneToOneField(Seat, related_name='ticket', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, blank=True, null=True, related_name='ticket1', on_delete=models.CASCADE)
    option_2 = models.ForeignKey(Option, blank=True, null=True, related_name='ticket2', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.flight}, {self.customer}, {self.seat}'


class GateRegistration(models.Model):
    ticket = models.OneToOneField(Ticket, related_name='registered', on_delete=models.CASCADE)
    is_registered = models.BooleanField(default=False)


class CheckIn(models.Model):
    ticket_gate = models.OneToOneField(GateRegistration, related_name='check_in', on_delete=models.CASCADE)
    is_registered = models.BooleanField(default=False)