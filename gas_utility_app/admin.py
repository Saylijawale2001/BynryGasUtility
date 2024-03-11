from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ServiceRequest, Account

admin.site.register(ServiceRequest)
admin.site.register(Account)
