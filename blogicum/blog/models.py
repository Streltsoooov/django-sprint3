from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone


User = get_user_model()
title_name = models.CharField('Заголовок', max_length=256)


class CustomOS(models.QuerySet):
    def published(self):
        return self.select_related(
            'category',
            'location',
            'author'
        ).filter(
            Q(is_published=True)
            & Q(pub_date__lte=timezone.now())
        )


class CustomManager(models.Manager):
    def get_queryset(self):
        return CustomOS(self.model)

    def annotate_comments_index(self):
        return self.get_queryset().published().filter(
            category__is_published=True
        )[0:5]

    def annotate_comments_category_posts(self, category_slug):
        return self.get_queryset().published().filter(
            category__slug=category_slug
        )


class BaseModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    title = title_name
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta():
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(BaseModel):
    name = models.CharField('Название места', max_length=256)

    class Meta():
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(BaseModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    title = title_name
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — можно делать '
        'отложенные публикации.')
    objects = CustomManager()

    class Meta():
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
