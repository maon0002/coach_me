from django.db import models


class Training(models.Model):
    MAX_SERVICE_NAME_LENGTH = 50
    service_name = models.CharField(
        max_length=MAX_SERVICE_NAME_LENGTH,
        default=None,
    )
    service_description = models.TextField(default="Add training description")
    service_image = models.URLField(default='https://freesvg.org/img/1380565395.png')

    inserted_on = models.DateTimeField(auto_now_add=True)  # ,  auto_now=True for update
    updated_on = models.DateTimeField(auto_now=True)  # ,  auto_now=True for update

    def __str__(self):
        return f'{self.service_name}'
        # return f'{self.id}: {self.service_name}'
