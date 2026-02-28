import pytest

from example.books.models import Book


@pytest.mark.count_queries
@pytest.mark.django_db
def test_index_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert len(resp.context["object_list"]) == 10


@pytest.mark.count_queries
@pytest.mark.django_db
def test_book_detail(client):
    book = Book.objects.get(id=1)
    resp = client.get(f"/{book.pk}/")
    assert resp.status_code == 200
    assert resp.context["object"] == book
