from django.contrib import admin

from main.models import Newsletter, Client


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('head', 'body', 'time', 'period', 'status', 'to_client', 'owner',)
    list_filter = ('status',)
    search_fields = ('owner', 'status',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'comment', 'owner',)
    list_filter = ('owner',)
    search_fields = ('owner',)

