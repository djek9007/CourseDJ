from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# Create your models here.
class Category(MPTTModel):
    """Модель категории"""
    name = models.CharField("имя", max_length=100)
    slug = models.SlugField("url", max_length=100, unique=True)
    description = models.TextField("описание", max_length=1000, default="", blank=True)
    parent = TreeForeignKey(
        'self',
        verbose_name="Родительская категория",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    template = models.CharField("шаблон", max_length=500, default="blog/post_list.html")
    published = models.BooleanField("отображать?", default=True)
    paginated = models.PositiveIntegerField("количество новостей на странице", default=5)
    sort = models.PositiveIntegerField('порядок', default=0)

    def __str__(self):
        return  self.name

    class Meta:
        verbose_name='Категория'
        verbose_name_plural='Категории'

class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField('Название тега', max_length=100, unique=True)
    slug = models.SlugField('url', max_length=100, unique=True)
    published = models.BooleanField("отображать?", default=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Post(models.Model):
    """Модель постов"""
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    title = models.CharField("заголовок", max_length=250)
    subtitle = models.CharField("под заголовок", max_length=500, blank=True, null=True)
    mini_text = models.TextField("описание")
    text = models.TextField("текст")
    create_date = models.DateTimeField("дата создания", auto_now=True)
    slug = models.SlugField("url", max_length=100, unique=True)
    tags = models.ManyToManyField(Tag, verbose_name="Тег", blank=True, related_name="tag")

    edit_date = models.DateTimeField(
        "дата редактирования",
        default=timezone.now,
        blank=True,
        null=True
    )
    published_date = models.DateTimeField(
        "дата публикации",
        default=timezone.now,
        blank=True,
        null=True
    )
    image = models.ImageField("главная фотография", upload_to="post/", null=True, blank=True)
    category = models.ForeignKey(Category, verbose_name="Категория",
                                 on_delete=models.CASCADE, null=True)
    template = models.CharField("шаблон", max_length=500, default="blog/post_list.html")
    published = models.BooleanField("опубликовать?", default=True)
    viewed = models.PositiveIntegerField("просмотрено", default=0)
    status = models.BooleanField("для зарегистрированных", default=False)
    sort = models.PositiveIntegerField('порядок', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новост"
        verbose_name_plural = "Новости"

    def get_absolute_url(self):
        return  reverse('detail_post', kwargs={'category': self.category.slug, 'slug': self.slug})

class Comment(models.Model):
    """Модель коментов"""
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    text = models.TextField('Коммент')
    post = models.ForeignKey(Post, verbose_name='Статья', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    moderation = models.BooleanField('Moderation', default=True)
    def __str__(self):
        return self.post


    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"