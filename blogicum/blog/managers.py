from django.db import models
from django.utils import timezone
from django.db.models import Q


class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.select_related(
            'category',
            'location',
            'author')

    def annotate_comments_index(self):
        return self.filter(
            Q(is_published=True)
            & Q(category__is_published=True)
            & Q(pub_date__lte=timezone.now())).order_by('-id')[0:5]

    def annotate_comments_post(self, category_slug):
        return self.filter(
            Q(category__slug=category_slug)
            & Q(is_published=True)
            & Q(pub_date__lte=timezone.now())
        )
