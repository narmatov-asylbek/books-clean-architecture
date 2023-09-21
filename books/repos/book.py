import abc
import datetime

from django.contrib.auth import get_user_model
from django.db.models import Avg, ObjectDoesNotExist, Case, When
from django.db.models import FloatField

from books.dtos import book as book_dtos
from books import models

User = get_user_model()


class IBookRepository(abc.ABC):

    def list_books(self, user: book_dtos.User,
                   created_before: datetime.datetime | None,
                   created_after: datetime.datetime | None,
                   authors: list[int] | None,
                   categories: list[str] | None) -> list[book_dtos.BookInfo]:
        raise NotImplementedError

    def get_book_detail(self, user: book_dtos.User,
                        book_id: int) -> book_dtos.BookDetail:
        raise NotImplementedError

    def add_to_favourite(self, user_id: int, book_id: int) -> None:
        raise NotImplementedError

    def create_review(self, user: book_dtos.User,
                      review: book_dtos.BookReview) -> book_dtos.BookReview:
        raise NotImplementedError

    def get_book_review(self, user_id: int,
                        book_id: int) -> book_dtos.BookReview | None:
        raise NotImplementedError

    def is_user_favourite(self, user_id: int, book_id: int) -> bool:
        raise NotImplementedError


class BookRepository(IBookRepository):

    def list_books(self, user: book_dtos.User,
                   created_before: datetime.datetime | None,
                   created_after: datetime.datetime | None,
                   authors: list[int] | None,
                   categories: list[str] | None) -> list[book_dtos.BookInfo]:
        filters = {}
        if created_before:
            filters["created_at__lte"] = created_before
        if created_after:
            filters["created_at__gte"] = created_after
        if authors:
            filters["author_id__in"] = authors
        if categories:
            filters["category__name__in"] = categories

        book_qs = models.Book.objects.all()
        if filters:
            book_qs = book_qs.filter(**filters)

        user = User.objects.get(id=user.id)
        book_qs = book_qs.annotate(avg_rating=Avg(
            'reviews__rating', output_field=FloatField(), default=0)).annotate(
                is_favourite=Case(When(users=user, then=True),
                                  default=False,
                                  output_field=FloatField()))
        books = []
        for book in book_qs.all():
            author_dto = book_dtos.Author(author_id=book.author.id,
                                          first_name=book.author.first_name,
                                          last_name=book.author.last_name,
                                          created_at=book.author.created_at)
            books.append(
                book_dtos.BookInfo(author=author_dto,
                                   category=book.category.name,
                                   name=book.name,
                                   id=book.id,
                                   favourite=book.is_favourite,
                                   average_rating=book.avg_rating))
        return books

    def get_book_detail(self, user: book_dtos.User,
                        book_id: int) -> book_dtos.BookDetail:
        book_db = models.Book.objects.get(id=book_id)

        is_favourite = book_db.users.filter(id=user.id).exists()
        average_rating = book_db.reviews.aggregate(
            avg_rating=Avg('rating', default=0))

        reviews = [
            book_dtos.BookReview(book_id=book_db.id,
                                 rating=review.rating,
                                 review=review.review,
                                 created_at=review.created_at)
            for review in models.BookReview.objects.filter(book=book_db)
        ]

        author_db = book_db.author
        author = book_dtos.Author(author_id=author_db.id,
                                  first_name=author_db.first_name,
                                  last_name=author_db.last_name,
                                  created_at=author_db.created_at)

        return book_dtos.BookDetail(
            id=book_db.id,
            name=book_db.name,
            category=book_db.category.name,
            description=book_db.description,
            created_at=book_db.created_at,
            author=author,
            reviews=reviews,
            favourite=is_favourite,
            average_rating=average_rating.get("avg_rating"))

    def is_user_favourite(self, user_id: int, book_id: int) -> bool:
        return User.objects.get(id=user_id).favourites.filter(
            id=book_id).exists()

    def get_book_review(self, user_id: int,
                        book_id: int) -> book_dtos.BookReview | None:
        try:
            review_db = models.BookReview.objects.get(user_id=user_id,
                                                      book_id=book_id)
        except ObjectDoesNotExist:
            return None
        return book_dtos.BookReview(book_id=review_db.book_id,
                                    rating=review_db.rating,
                                    review=review_db.review,
                                    created_at=review_db.created_at)

    def create_review(self, user: book_dtos.User,
                      review: book_dtos.BookReview) -> book_dtos.BookReview:
        models.Book.objects.get(id=review.book_id)
        created = models.BookReview.objects.create(user_id=user.id,
                                                   book_id=review.book_id,
                                                   review=review.review,
                                                   rating=review.rating)
        review.created_at = created.created_at
        return review

    def add_to_favourite(self, user_id: int, book_id: int) -> None:
        book = models.Book.objects.get(id=book_id)
        User.objects.get(id=user_id).favourites.add(book)
