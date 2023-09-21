import dataclasses
import datetime


@dataclasses.dataclass
class Category:
    id: str
    name: str


@dataclasses.dataclass
class Author:
    author_id: int
    first_name: str
    last_name: str
    created_at: datetime.datetime | None = None

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"


@dataclasses.dataclass
class BookInfo:
    id: int
    name: str
    category: str
    author: Author
    average_rating: int = 0
    favourite: bool = False


@dataclasses.dataclass
class BookReview:
    book_id: int
    rating: int
    review: str
    created_at: datetime.datetime | None = None


@dataclasses.dataclass
class BookDetail:
    id: int
    name: str
    category: str
    author: Author
    description: str
    created_at: datetime.datetime
    reviews: list[BookReview] = dataclasses.field(default_factory=list)
    average_rating: int = 0
    favourite: bool = False


@dataclasses.dataclass
class User:
    id: int
    email: str
