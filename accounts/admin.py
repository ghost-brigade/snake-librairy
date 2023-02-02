from django.contrib import admin
from .models import User, CustomerUser, BookSellerUser
# Register your models here.
admin.site.register(User)
admin.site.register(CustomerUser)
admin.site.register(BookSellerUser)
