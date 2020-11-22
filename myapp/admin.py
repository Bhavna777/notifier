from django.contrib import admin

# Register your models here.

from .models import Send, Recieve

admin.site.register(Send)
admin.site.register(Recieve)