from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView
from datetime import datetime, timedelta

from core.models import Reservation, Library
from .forms import CreateUserForm, UpdateUserForm
from core.models import Reservation
from .models import CustomerUser, BookSellerUser, User


# Create your views here.
class CustomerSignUpView(CreateView):
    """
    Creates new employee
    """
    template_name = 'account/customer_signup.html'
    form_class = CreateUserForm

    def get(self, request, *args, **kwargs):
        # Use RequestContext instead of render_to_response from 3.0
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer = True
            # user.set_password(form.cleaned_data['password'])
            user.save()
            CustomerUser.objects.create(user=user)

            # user = U.objects.get(email=user.email)
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class BookSellerSignUpView(CreateView):
    """
    Creates new employee
    """
    template_name = 'account/book_seller_signup.html'
    form_class = CreateUserForm

    def get(self, request, *args, **kwargs):
        # Use RequestContext instead of render_to_response from 3.0
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_bookseller = True
            # user.set_password(form.cleaned_data['password'])
            user.save()
            BookSellerUser.objects.create(user=user)

            library = Library.objects.create(name=user.username + ' library', user=user)

            # user = U.objects.get(email=user.email)
            return redirect('login')
        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect("/")


def profile(request):
    user_profile = get_object_or_404(User, id=request.user.id)

    if user_profile.is_superuser:
        user_profile.role = 'Administrateur'
    elif user_profile.is_bookseller:
        user_profile.role = 'Libraire'
    elif user_profile.is_customer:
        user_profile.role = 'Client'

    form_class = UpdateUserForm
    context = {'user_profile': user_profile, 'form': form_class}

    if request.method == 'POST':
        form = form_class(data=request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')

    return render(request, 'user_profile.html', context, )

def reservation(request):
    user_profile = get_object_or_404(User, id=request.user.id)
    reservations = Reservation.objects.filter(user=user_profile)
    context = {'user_profile': user_profile, 'reservations': reservations}

    for reservation in reservations:
        today = datetime.now().date()
        diff = reservation.limit_date - today
        if(diff.days < 1):
            reservation.days_left = 'La date limite a expiré'
        else:
            reservation.days_left = 'Il vous reste ' + str(diff.days) + ' jours pour rendre votre livre'

    return render(request, 'reservation/my_reservation.html', context)