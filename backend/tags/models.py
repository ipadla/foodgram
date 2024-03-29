import re

from django.core.validators import RegexValidator
from django.db import models


class Tags(models.Model):  # TODO: Rename to Tag
    name = models.CharField(max_length=64, unique=True, db_index=True)

    color = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(regex='^#?[A-Fa-f0-9]{6}$')
        ],
        unique=True
    )

    slug = models.SlugField(unique=True, db_index=True)

    class Meta:
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Если не указан символ диез - добавляем его
        # Всю строку переводим в прописные буквы
        if re.match('^#[A-Fa-f0-9]{6}$', self.color):
            self.color = self.color.lower()
        else:
            self.color = f'#{self.color.lower()}'

        super().save(*args, **kwargs)
