from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from reviews.validators import validate_year


class Category(models.Model):
    """Модель категории произведения."""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Genre(models.Model):
    """Модель жанра произведений."""
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска произведения',
        validators=[validate_year],

    )
    description = models.TextField(
        verbose_name='Описание произведения',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )
    rating = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.genre} - {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Оценка не может быть меньше 1'),
            MaxValueValidator(10, 'Оценка не может быть выше 10'),
        ],
        verbose_name='Рейтинг',

    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['title', 'author']
        ordering = ('-pub_date',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_title_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_title_rating()

    def update_title_rating(self):
        average_rating = self.title.reviews.aggregate(
            models.Avg('score'))['score__avg']
        if average_rating is not None:
            self.title.rating = round(average_rating)
        else:
            self.title.rating = 0
        self.title.save()


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )

    class Meta:
        """Мета класс комментария."""

        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

