from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Author(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=200)
    last_name = models.CharField(verbose_name="Фамилия", max_length=200)
    created_at = models.DateTimeField(verbose_name="Дата создания",
                                      auto_now_add=True)

    class Meta:
        db_table = "authors"
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        unique_together = ("first_name", "last_name")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class BookReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name="Автор отзыва",
                             related_name="reviews")
    book = models.ForeignKey("books.Book",
                             on_delete=models.CASCADE,
                             verbose_name="Книга",
                             related_name="reviews")
    rating = models.IntegerField(
        verbose_name="Рейтинг",
        validators=[MaxValueValidator(5),
                    MinValueValidator(1)])
    review = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateTimeField(verbose_name="Дата создания",
                                      auto_now_add=True)

    class Meta:
        db_table = "reviews"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ("user_id", "book_id")

    def __str__(self):
        return f"{self.id} {self.book.name}"


class Category(models.Model):
    name = models.CharField(verbose_name="Название",
                            max_length=300,
                            unique=True)

    class Meta:
        db_table = "categories"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey("books.Author",
                               verbose_name="Автор",
                               related_name="books",
                               on_delete=models.CASCADE)
    category = models.ForeignKey("books.Category",
                                 verbose_name="Категория",
                                 related_name="books",
                                 on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=300)
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(verbose_name="Дата создания",
                                      auto_now_add=True)

    class Meta:
        db_table = "books"
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.name
