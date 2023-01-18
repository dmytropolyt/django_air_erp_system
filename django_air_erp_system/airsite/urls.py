from django.urls import path, re_path
from .views import DestinationFormView, TicketCreateView, TicketSuccessView

urlpatterns = [
    path('', DestinationFormView.as_view(), name='home'),
    path('ticket/success/', TicketSuccessView.as_view(), name='ticket-success'),
    re_path(r'^ticket/+', TicketCreateView.as_view(), name='ticket-create'),
]