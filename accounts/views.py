from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView

from .forms import CreateUserForm
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

            # user = U.objects.get(email=user.email)
            return redirect('login')
        return render(request, self.template_name, {'form': form})


def logout_view(request):
    logout(request)
    return redirect("/")


def profile(request):
    user_profile = get_object_or_404(User, id=request.user.id)
    context = {'user_profile': user_profile}

    return render(request, 'user_profile.html', context)
