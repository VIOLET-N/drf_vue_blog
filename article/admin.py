from django.contrib import admin

# Register your models here.
from article.models import Article, Tag, Category

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Category)
