from dataclasses import asdict
from rest_framework import serializers
from books.dtos import book as book_dtos


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    @classmethod
    def from_dto(cls, dto: book_dtos.Category):
        return cls(id=dto.id, name=dto.name)


class AuthorSerializer(serializers.Serializer):
    author_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    created_at = serializers.DateTimeField()

    @classmethod
    def from_dto(cls, dto: book_dtos.Author) -> 'AuthorSerializer':
        return cls(asdict(dto))


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    category = serializers.CharField()
    author = AuthorSerializer()
    average_rating = serializers.IntegerField()
    favourite = serializers.BooleanField()

    @classmethod
    def from_dto(cls, dto: book_dtos.BookInfo) -> 'BookSerializer':
        author = AuthorSerializer.from_dto(dto.author)
        return cls(author=author,
                   favourite=dto.favourite,
                   average_rating=dto.average_rating,
                   id=dto.id,
                   name=dto.name,
                   category=dto.category)


class BookReviewCreateSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    review = serializers.CharField()


class BookReviewSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    review = serializers.CharField()
    created_at = serializers.DateTimeField(required=True)

    @classmethod
    def from_dto(cls, dto: book_dtos.BookReview) -> 'BookReviewSerializer':
        return cls(book_id=dto.book_id,
                   rating=dto.rating,
                   review=dto.review,
                   created_at=dto.created_at)


class BookDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    category = serializers.CharField()
    author = AuthorSerializer()
    average_rating = serializers.IntegerField()
    favourite = serializers.BooleanField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField(required=True)
    reviews = BookReviewSerializer(many=True)

    @classmethod
    def from_dto(cls, dto: book_dtos.BookDetail) -> 'BookDetailSerializer':
        return cls(asdict(dto))


class FavouriteCreateSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
