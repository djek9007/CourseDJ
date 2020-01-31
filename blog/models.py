from django.db import models

# Create your models here.
class Category(models.Model):
    """Модель категории"""
    name = models.CharField(max_length=100, verbose_name='Имя')
    slug = models.SlugField('url', max_length=100)

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категории'