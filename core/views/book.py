from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from core.forms import AddBookForm, BookReservationForm
from core.models import Book, Reservation, BookLibrary


class BookList(ListView):
    model = Book
    queryset = Book.objects.all()
    template_name = 'book/list.html'
    context_object_name = 'books'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            qs = Book.objects.filter(Q(title__icontains=query) | Q(
                author__first_name__icontains=query))

            return qs
        return qs


class BookUserList(LoginRequiredMixin, ListView):
    model = Book
    queryset = Book.objects.all()
    template_name = 'book/list_user.html'
    context_object_name = 'books'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        qs = Book.objects.filter(author=self.request.user)
        return qs




class BookAdd(CreateView):
    template_name = 'book/add_book.html'
    form_class = AddBookForm

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

            # user = U.objects.get(email=user.email)
            return redirect('/')
        return render(request, self.template_name, {'form': form})


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        try:
            return qs.filter(author=self.request.user)
        except Exception:
            raise PermissionError("You Don't Have A Permission for this View.")


class BookUpdate(OwnerMixin, SuccessMessageMixin, UpdateView):
    model = Book
    form_class = AddBookForm
    context_object_name = 'books'
    template_name = 'book/update_form.html'
    success_message = "Book is updated."
    success_url = reverse_lazy('book_list')

class BookReservation(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = BookReservationForm
    template_name = 'reservation/add_reservation.html'
    success_url = reverse_lazy('book_list')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        # Use RequestContext instead of render_to_response from 3.0
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            book_library = BookLibrary.objects.get(id=kwargs['pk'])
            if book_library.collection > 0:
                book_library.collection -= 1
                book_library.save()
                reservation = form.save(commit=False)
                reservation.book_library = book_library
                reservation.user = request.user
                reservation.limit_date = form.cleaned_data['limit_date']
                reservation.save()

            return redirect('/')
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookAddLibrary(CreateView):
    template_name = 'book/add_book_library.html'
    form_class = AddBookForm

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated and request.user.is_bookseller:
            return render(request, self.template_name, {
                'form': self.form_class(),
            })

        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_bookseller:
            form = self.form_class(request.POST, request.FILES)

            if form.is_valid():


                return redirect('/')
            return render(request, self.template_name, {'form': form})

        return HttpResponseForbidden()