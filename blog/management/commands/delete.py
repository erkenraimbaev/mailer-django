from django.core.management import BaseCommand

from blog.models import Blog


class Command(BaseCommand):

    def handle(self, *args, **options):
        Blog.truncate_table_restart_id()