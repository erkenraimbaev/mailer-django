from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'post_content', 'image', 'date_of_create', 'publication_sign', 'count_of_views',
                    'owner',)
    list_filter = ()
    search_fields = ('slug', 'post_content',)
