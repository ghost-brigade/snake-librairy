from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .forms import AddBookForm
from .models import Book


# Create your views here.

class AddBookView(CreateView):
    template_name = 'add_book.html'
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


class BookListView(ListView):
    model = Book
    queryset = Book.objects.all()
    template_name = 'book_list.html'
    context_object_name = 'book_list'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            qs = Book.objects.filter(Q(book_title__icontains=query) | Q(
                author__first_name__icontains=query))

            return qs
        return qs


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        try:
            return qs.filter(author=self.request.user)
        except Exception:
            raise PermissionError("You Don't Have A Permission for this View.")


class CurrentBookListView(LoginRequiredMixin, ListView):
    model = Book
    queryset = Book.objects.all()
    template_name = 'current_user_book_list.html'
    context_object_name = 'book_list'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        qs = Book.objects.filter(author=self.request.user)
        return qs


class BookUpdateView(OwnerMixin, SuccessMessageMixin, UpdateView):
    model = Book
    form_class = AddBookForm
    context_object_name = 'update_book'
    template_name = 'book_update_form.html'
    success_message = "Book is updated."
    success_url = reverse_lazy('book_list')
