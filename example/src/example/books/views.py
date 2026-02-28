from django.views import generic

from .models import Book


class IndexView(generic.ListView):
    template_name = "books/index.html"
    model = Book


class DetailView(generic.DetailView):
    model = Book
    template_name = "books/detail.html"
