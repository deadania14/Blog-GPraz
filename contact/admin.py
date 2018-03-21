from django.contrib import admin
from .models import VisitorMessage

class VisitorMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    ordering = ('-created_at', )
    list_filter = ('created_at', )

# Register your models here.
admin.site.register(VisitorMessage, VisitorMessageAdmin)