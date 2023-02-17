from django.contrib import admin
from sales.models import Sale, Article, ArticleCategory
# Register your models here.

admin.site.register(Sale)
admin.site.register(Article)
admin.site.register(ArticleCategory)
