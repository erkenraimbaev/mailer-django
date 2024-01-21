from django.urls import path

from blog.views import BlogListView
from main.apps import MainConfig
from main.views import NewsletterCreateView, NewsletterListView, ContactsView, NewsletterDetailView, \
    NewsletterUpdateView, NewsletterDeleteView, ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, \
    ClientDeleteView

app_name = MainConfig.name


urlpatterns = [
    path('create_newsletter/', NewsletterCreateView.as_view(), name='create_newsletter'),
    path('', BlogListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('newsletter/', NewsletterListView.as_view(), name='newsletters'),
    path('newsletter/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter'),
    path('edit/<int:pk>', NewsletterUpdateView.as_view(), name='edit_newsletter'),
    path('delete_newsletter/<int:pk>', NewsletterDeleteView.as_view(), name='delete_newsletter'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('clients/', ClientListView.as_view(), name='clients'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client'),
    path('edit/<int:pk>', ClientUpdateView.as_view(), name='edit_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
]
