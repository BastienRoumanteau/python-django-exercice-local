from django.urls import path, include
from sales.views import (
    SaleAPIView,
    ArticleAPIView
)

urlpatterns = [
    path('', SaleAPIView.as_view()),
    path('articles/', ArticleAPIView.as_view()),
]
