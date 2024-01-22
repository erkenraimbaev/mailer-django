from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import ProductForm
from blog.models import Blog


# Create your views here.
class BlogCreateView(CreateView):
    model = Blog
    form_class = ProductForm
    fields = ('title', 'post_content', 'image')
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.slug = slugify(new_post.title)
        new_post.save()
        return super().form_valid(form)


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_of_views += 1
        self.object.save()
        return self.object


class BlogListView(ListView):
    model = Blog
    blog_list = Blog.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication_sign=True)
        return queryset


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = ProductForm

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.slug = slugify(new_post.title)
        new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:home')


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')


def toggle_activity(request, pk):
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.publication_sign:
        blog_item.publication_sign = False
    else:
        blog_item.publication_sign = True
    blog_item.save()
    return redirect(reverse('blog:list'))
