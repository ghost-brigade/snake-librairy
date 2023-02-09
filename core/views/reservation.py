from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from core.models import Reservation

class ReservationAdd(LoginRequiredMixin, CreateView):
    model = Reservation
    fields = ['book', 'limit_date']
    template_name = 'reservation/add_reservation.html'
    success_url = reverse_lazy('book_list')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_customer:
            return HttpResponseForbidden()
        # Use RequestContext instead of render_to_response from 3.0
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_customer:
            return HttpResponseForbidden()
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.author = request.user
            # user.set_password(form.cleaned_data['password'])
            user.save()
