from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('add/book/', views.AddBookView.as_view(), name='add_book'),
    path('current/user/books/',
         views.CurrentBookListView.as_view(), name='current_user'),
    path('book/update/<int:pk>/', views.BookUpdateView.as_view(), name='update_book'),
]
