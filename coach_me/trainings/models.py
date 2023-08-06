from django.db import models
from django.utils.text import slugify


class Training(models.Model):
    MAX_SERVICE_NAME_LENGTH = 50
    SLUG_MAX_LENGTH = 254

    service_name = models.CharField(
        max_length=MAX_SERVICE_NAME_LENGTH,
        default=None,
    )
    service_description = models.TextField(default="Add training description")
    service_image = models.URLField(default='https://freesvg.org/img/1380565395.png')

    slug = models.SlugField(
        max_length=SLUG_MAX_LENGTH,
        unique=True,
        blank=True)

    inserted_on = models.DateTimeField(auto_now_add=True)  # ,  auto_now=True for update
    updated_on = models.DateTimeField(auto_now=True)  # ,  auto_now=True for update

    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            self.slug = slugify(f"{self.pk}-{self.service_name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.service_name}'

