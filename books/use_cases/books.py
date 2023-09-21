from datetime import datetime

from books.dtos.book import BookDetail, User, BookReview, BookInfo
from books.repos.book import IBookRepository
from books.exceptions import AlreadyExistsException


def list_books_use_case(repo: IBookRepository, user: User,
                        created_before: datetime | None,
                        created_after: datetime | None,
                        authors: list[str] | None,
                        categories: list[str] | None) -> list[BookInfo]:
    return repo.list_books(user=user,
                           created_before=created_before,
                           created_after=created_after,
                           authors=authors,
                           categories=categories)


def get_book_use_case(repo: IBookRepository, user: User,
                      book_id: int) -> BookDetail:
    return repo.get_book_detail(user=user, book_id=book_id)


def add_to_favourite_use_case(repo: IBookRepository, user: User,
                              book_id: int) -> None:
    if repo.is_user_favourite(user_id=user.id, book_id=book_id):
        raise AlreadyExistsException(message="Уже добавлен в избранные")
    return repo.add_to_favourite(user_id=user.id, book_id=book_id)


def create_review_use_case(repo: IBookRepository, user: User,
                           review: BookReview) -> BookReview:
    if repo.get_book_review(user_id=user.id, book_id=review.book_id):
        raise AlreadyExistsException(message="Пользователь уже оставил отзыв")
    return repo.create_review(user=user, review=review)
