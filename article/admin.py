from django.contrib import admin

# Register your models here.
from article.models import Article, Tag, Category, Avatar

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Avatar)
