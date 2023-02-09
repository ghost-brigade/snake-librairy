from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, CreateView

from core.forms import AddBookLibraryForm
from core.models import BookLibrary, Library


class LibraryDashboard(ListView):
    model = BookLibrary
    template_name = 'dashboard/list.html'
    context_object_name = 'booksLibrary'
    queryset = BookLibrary.objects.all()

    def get_queryset(self):
        qs = BookLibrary.objects.filter(Q(library__user=self.request.user))
        query = self.request.GET.get('search')
        if query:
            qs = BookLibrary.objects.filter(Q(book__title__icontains=query) and Q(library__user=self.request.user))

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
