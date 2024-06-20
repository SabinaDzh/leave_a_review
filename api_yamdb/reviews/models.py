from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from reviews.constants import MAX_LENGTH_NAME, MAX_LENGTH_SLUG
from reviews.validators import validate_year


class Category(models.Model):
    """Модель категории произведения."""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=MAX_LENGTH_NAME,
    )
    slug = models.SlugField(
        verbose_name='Слаг категории',
        max_length=MAX_LENGTH_SLUG,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Genre(models.Model):
    """Модель жанра произведений."""
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=MAX_LENGTH_NAME,
    )
    slug = models.SlugField(
        verbose_name='Слаг жанра',
        max_length=MAX_LENGTH_SLUG,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=MAX_LENGTH_NAME,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска произведения',
        validators=(validate_year,),
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель связи жанров и произведений."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles',
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
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author')
        ]
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
            self.title.rating = None
        self.title.save()

    def __str__(self):
        return f"Отзыв от {self.author} о {self.title}"


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

    def __str__(self):
        return f"Коссентарий от {self.author} для {self.review}"
