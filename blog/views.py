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

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication_sign=True)
        return queryset


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = ProductForm
    fields = ('title', 'post_content', 'image')

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.slug = slugify(new_post.title)
        new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
