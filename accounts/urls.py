from django.urls import path
from . import views

urlpatterns = [
    path('customer/signup/', views.CustomerSignUpView.as_view(),
         name='customer_signup'),
    path('bookseller/signup/', views.BookSellerSignUpView.as_view(),
         name='bookseller_signup'),
    path('profile/', views.profile, name='user_profile'),
    path('profile/reservation', views.reservation, name='user_reservation'),
    path("logout/", views.logout_view, name='logout'),

]
