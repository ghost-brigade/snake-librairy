from django.db.models import Q
from django.views.generic import ListView
from core.models import Library, BookLibrary


class LibraryList(ListView):
    model = Library
    queryset = Library.objects.all()
    template_name = 'library/list.html'
    context_object_name = 'libraries'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            qs = Library.objects.filter(Q(name__icontains=query))

            return qs
        return qs


class LibraryGet(ListView):
    model = Library
    queryset = Library.objects.all()
    template_name = 'library/detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('search')


        context = super().get_context_data(**kwargs)
        context['booksLibrary'] = self.get_queryset().booklibrary_set.filter(
            library=self.kwargs['id'],
            book_available=True,
            collection__gte=1
        )
        if query:
            context['booksLibrary'] = self.get_queryset().booklibrary_set.filter(
                library=self.kwargs['id'],
                book__title__icontains=query,
                book_available=True,
                collection__gte=1,
            )
        return context


    def get_queryset(self):
        query = self.kwargs['id']
        qs = Library.objects.get(pk=query)

        return qs



