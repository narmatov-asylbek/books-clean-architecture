from django.urls import path
from books.api import views

urlpatterns = [
    path("", views.get_book_list, name="list-books"),
    path("<int:book_id>/", views.get_book_detail, name="book-detail"),
    path("favourites/", views.add_to_favourite, name='add-favourite'),
    path("reviews/", views.create_review, name="create-review")
]
