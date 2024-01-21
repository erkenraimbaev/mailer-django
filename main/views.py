from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, DeleteView, DetailView

from main.forms import NewsletterForm, ClientForm
from main.models import Newsletter, Client


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()


class NewsletterDetailView(DetailView):
    model = Newsletter

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class NewsletterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('main:home')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_staff:
            return self.object
        raise Http404

    # def form_valid(self, form):
    #     formset = self.get_context_data()['formset']
    #     self.object = form.save()
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #     return super().form_valid(form)

    def test_func(self):
        return self.get_object().owner == self.request.user or self.request.user.is_superuser \
            or self.request.user.has_perms(['main.change_newsletter'])


class NewsletterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy('main:home')
    permission_required = "main.delete_newsletter"


@login_required
def post(request, *args, **kwargs):
    name = request.POST.get('name')
    phone_number = request.POST.get('phone')
    message = request.POST.get('message')
    print(f'Имя: {name}\nНомер телефона: {phone_number}\nСообщение: {message}')
    return redirect(reverse('main:contacts'))


class ContactsView(LoginRequiredMixin, TemplateView):
    template_name = 'contacts.html'
    extra_context = {
        'title': 'Контакты'
    }


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'main/client_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        return context_data


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = NewsletterForm
    success_url = reverse_lazy('main:home')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_staff:
            return self.object
        raise Http404

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().owner == self.request.user or self.request.user.is_superuser \
            or self.request.user.has_perms(['main.change_client'])


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main:home')
    permission_required = "main.delete_client"
