from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from core.forms import AddBookLibraryForm, UpdateBookLibraryForm
from core.models import BookLibrary, Library, Reservation


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        try:
            return qs.filter(library__user=self.request.user)
        except Exception:
            raise PermissionError("You Don't Have A Permission for this View.")


class LibraryDashboard(ListView):
    model = BookLibrary
    template_name = 'dashboard/list.html'
    context_object_name = 'booksLibrary'
    queryset = BookLibrary.objects.all()

    def get_queryset(self):
        qs = BookLibrary.objects.filter(Q(library__user=self.request.user))
        query = self.request.GET.get('search')

        if query:
            qs = BookLibrary.objects.filter(Q(book__title__startswith=query) and Q(library__user=self.request.user))

            return qs
        return qs


class LibraryDashboardAdd(CreateView):
    template_name = 'dashboard/add_book_library.html'
    form_class = AddBookLibraryForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_bookseller:
            return render(request, self.template_name, {'form': self.form_class})
        return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_bookseller:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                bookLibrary = form.save(commit=False)
                bookLibrary.library = Library.objects.get(user=request.user)
                bookLibrary.save()

                return redirect('dashboard')
            return render(request, self.template_name, {'form': form})

        return HttpResponseForbidden()


class LibraryDashboardUpdate(OwnerMixin, SuccessMessageMixin, UpdateView):
    model = BookLibrary

    # remove field book from form
    form_class = UpdateBookLibraryForm
    context_object_name = 'booksLibrary'
    template_name = 'dashboard/update_book_library.html'
    success_message = "Book in your library is updated."
    success_url = reverse_lazy('dashboard')


class LibraryDashboardDelete(OwnerMixin, SuccessMessageMixin, DeleteView):
    model = BookLibrary
    context_object_name = 'booksLibrary'
    success_message = "Book in your library is deleted."
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = self.success_message
        self.object.delete()
        return redirect(self.success_url)


class LoanDashboard(ListView):
    model = Reservation
    template_name = 'dashboard/loan/list.html'
    context_object_name = 'reservations'
    queryset = Reservation.objects.all()

    def get_queryset(self):
        qs = Reservation.objects.filter(Q(book_library__library__user=self.request.user))
        return qs


class LoanDashboardUpdate(SuccessMessageMixin, UpdateView):
    model = Reservation
    fields = ['status']
    context_object_name = 'reservations'
    template_name = 'dashboard/loan/update.html'
    success_message = "Book in your library is updated."
    success_url = reverse_lazy('dashboard_loan')