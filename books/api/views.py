import datetime

from dataclasses import asdict

from django.db.models import ObjectDoesNotExist
from rest_framework.views import Request
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from books.exceptions import AlreadyExistsException

from books.repos.book import BookRepository
from books.api.serializers import BookDetailSerializer, BookReviewCreateSerializer, BookSerializer, FavouriteCreateSerializer
from books.use_cases.books import add_to_favourite_use_case, get_book_use_case, list_books_use_case, create_review_use_case
from books.dtos.book import BookReview


@swagger_auto_schema(
    method="get",
    description="Get the list of the books",
    manual_parameters=[
        openapi.Parameter("category",
                          openapi.IN_QUERY,
                          description="Filter by category",
                          type=openapi.TYPE_ARRAY,
                          items=openapi.Items(type=openapi.TYPE_STRING)),
        openapi.Parameter("author",
                          openapi.IN_QUERY,
                          description="Filter by author",
                          type=openapi.TYPE_ARRAY,
                          items=openapi.Items(type=openapi.TYPE_INTEGER)),
        openapi.Parameter(
            "created_before",
            openapi.IN_QUERY,
            description="Get books created before date. Format in Y-m-d",
            type=openapi.TYPE_STRING),
        openapi.Parameter("created_after",
                          openapi.IN_QUERY,
                          description="Get books created before date",
                          type=openapi.TYPE_STRING),
    ],
    responses={200: BookSerializer(many=True)})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_book_list(request: Request):
    category_param = request.GET.get("category")
    author_param = request.GET.get("author")
    created_before_param: str | None = request.GET.get("created_before")
    created_after_param: str | None = request.GET.get("created_after")

    authors: list[int] | None = None
    if author_param:
        authors = [int(author_id) for author_id in author_param.split(",")]

    categories: list[str] | None = None
    if category_param:
        categories = category_param.split(",")

    created_before = None
    if created_before_param:
        created_before = datetime.datetime.strptime(created_before_param,
                                                    "%Y-%m-%d")
        created_before = created_before.replace(tzinfo=datetime.timezone.utc)
        created_before = datetime.datetime.combine(created_before,
                                                   datetime.time.max)
    created_after = None
    if created_after_param:
        created_after = datetime.datetime.strptime(created_after_param,
                                                   "%Y-%m-%d")
        created_after = created_after.replace(tzinfo=datetime.timezone.utc)
        created_after = datetime.datetime.combine(created_after,
                                                  datetime.time.min)

    repo = BookRepository()
    books = list_books_use_case(repo=repo,
                                user=request.user,
                                categories=categories,
                                authors=authors,
                                created_before=created_before,
                                created_after=created_after)
    converted_books = [asdict(book) for book in books]
    serializer = BookSerializer(data=converted_books, many=True)
    serializer.is_valid(raise_exception=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method="get",
                     description="Get Book detail",
                     responses={200: BookDetailSerializer()})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_book_detail(request: Request, book_id: int):

    repo = BookRepository()
    try:
        book = get_book_use_case(repo=repo, user=request.user, book_id=book_id)
    except ObjectDoesNotExist:
        raise ValidationError("Книга не найдена")

    serializer = BookDetailSerializer.from_dto(book)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method="post",
                     description="Add book to favourites",
                     responses={200: FavouriteCreateSerializer()},
                     request_body=FavouriteCreateSerializer())
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_favourite(request: Request):
    data = FavouriteCreateSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    repo = BookRepository()
    try:
        add_to_favourite_use_case(repo=repo,
                                  user=request.user,
                                  book_id=data.validated_data["book_id"])
    except AlreadyExistsException:
        raise ValidationError("Уже в избранных")
    except ObjectDoesNotExist:
        raise ValidationError("Книга не найдена")

    return Response(data=data.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method="post",
                     description="Create a review for a book",
                     responses={200: BookReviewCreateSerializer()},
                     request_body=BookReviewCreateSerializer())
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_review(request: Request):
    data = BookReviewCreateSerializer(data=request.data)
    data.is_valid(raise_exception=True)
    repo = BookRepository()
    review = BookReview(book_id=data.validated_data["book_id"],
                        rating=data.validated_data["rating"],
                        review=data.validated_data["review"])
    try:
        create_review_use_case(repo, user=request.user, review=review)
    except AlreadyExistsException:
        raise ValidationError("Вы уже оставили отзыв")
    except ObjectDoesNotExist:
        raise ValidationError("Книга не найдена")

    return Response(data=data.data, status=status.HTTP_200_OK)
