from django.urls import path
from . import views

book_name_prefix = 'book'
library_name_prefix = 'library'

urlpatterns = [
    path('book', views.book.BookList.as_view(), name=book_name_prefix + '_list'),
    path('book/my-list', views.book.BookUserList.as_view(), name=book_name_prefix + '_list_user'),
    path('book/add', views.book.BookAdd.as_view(), name=book_name_prefix + '_add'),
    path('book/update/<int:pk>/', views.book.BookUpdate.as_view(), name=book_name_prefix + '_update'),
    path('book/reservation/<int:pk>/', views.book.BookReservation.as_view(), name=book_name_prefix + '_reservation'),

    path('', views.library.LibraryList.as_view(), name=library_name_prefix + '_list'),
    path('<int:id>', views.library.LibraryGet.as_view(), name=library_name_prefix + '_get'),
]
