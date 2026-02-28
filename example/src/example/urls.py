from django.urls import include, path

urlpatterns = [
    path("", include("example.books.urls")),
]
