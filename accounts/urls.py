from django.urls import path
from . import views

urlpatterns = [
    path('customer/signup/', views.CustomerSignUpView.as_view(),
         name='customer_signup'),
    path('bookseller/signup/', views.BookSellerSignUpView.as_view(),
         name='bookseller_signup'),
    path('user/profile/', views.profile, name='user_profile'),
    path("logout/", views.logout_view, name='logout'),

]
