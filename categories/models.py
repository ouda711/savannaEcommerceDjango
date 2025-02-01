from django.db import models
# Create your models here.
from django.utils.text import slugify

from shared.models import TimestampedModel


def gent_random_category():
    return Category.objects.order_by('?').first()


class CategoryManager(models.Manager):
    pass


class Category(TimestampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)
    description = models.CharField(max_length=140)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    objects = CategoryManager()

    def save(self, *args, **kwargs):
        # Create a slug combining parent name and current category name
        if self.parent:
            self.slug = slugify(f"{self.parent.name}-{self.name}")
        else:
            self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name