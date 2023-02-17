from rest_framework import serializers
from sales.models import Sale, Article


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ("id", "date", "author", "article",
                  "quantity", "unit_selling_price")


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id", "code", "category", "name", "manufacturing_cost")
