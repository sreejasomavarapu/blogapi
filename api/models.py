from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from matplotlib.pyplot import title
from autoslug import AutoSlugField
import uuid
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    STATUS_OPTIONS =(
        ('published','Published'),
        ('draft','Draft'),

    )

    title=models.CharField(max_length=100)
    body = models.TextField(max_length=200)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    slug = AutoSlugField(populate_from='title')
    image = models.ImageField()
    # if i put unique = True im getting error as unique constraint failed
    # The reason for this constrain could be that you didn't have any field called slug in Category class when you have initially migrated it (First Migration), and after adding this field in the model, when you ran makemigrations, you have set default value to something static value(i.e None or '' etc), and which broke the unique constrain for the Category's table's slug column in which slug should be unique but it isn't because all the entry will get that default value.
    published_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_OPTIONS,max_length=50)

    objects = models.Manager()
    postobjects = PostObjects()

    class Meta:
        ordering =('-published_date',)

    def __str__(self) -> str:
        return self.title

