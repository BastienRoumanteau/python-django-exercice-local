from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from sales.models import Sale, Article
from sales.serializers import SaleSerializer
from sales.serializers import ArticleSerializer
from rest_framework.renderers import JSONRenderer
from operator import attrgetter

from rest_framework import pagination


class SaleAPIView(APIView):

    def get(self, request):
        '''
        Get all sales
        '''
        arrayPagination = 25
        page = int(request.query_params.get('page'))
        sales = Sale.objects.filter(author=request.user.id)[
            page * arrayPagination: page * arrayPagination + arrayPagination]
        serializer = SaleSerializer(sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
        Create a sale with the given data
        '''
        data = {
            'date': request.data.get('date'),
            'article': request.data.get('article'),
            'quantity': request.data.get('quantity'),
            'author': request.user.id,
            'unit_selling_price': request.data.get('unit_selling_price'),
        }
        serializer = SaleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        '''
        Delete a sale with the given id
        '''
        sale = Sale.objects.filter(
            id=request.query_params.get('id'), author=request.user.id)

        if sale:
            sale.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        '''
        Update a sale with the given data
        '''
        sale = Sale.objects.filter(
            id=request.query_params.get('id'), author=request.user.id).first()

        if not sale:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = {
            'date': request.data.get('date'),
            'article': sale.article.id if request.data.get('article') is None else request.data.get('article'),
            'quantity': request.data.get('quantity'),
            'unit_selling_price': request.data.get('unit_selling_price'),
        }
        serializer = SaleSerializer(
            instance=sale, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleAPIView(APIView):
    # def get(self, request):
    #     '''
    #     Get all articles
    #     '''
    #     articles = Article.objects.all()
    #     serializer = ArticleSerializer(articles, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        '''
        Get aggregated articles
        '''
        arrayPagination = 25
        page = int(request.query_params.get('page'))
        articles = Article.objects.all()[
            page * arrayPagination: page * arrayPagination + arrayPagination]

        # serializer = ArticleSerializer(articles, many=True)
        array = []
        for article in articles:
            sales = Sale.objects.filter(article=article.id)
            serializer = SaleSerializer(sales, many=True)

            sum = 0
            totalManufacturing = int(
                article.manufacturing_cost) * int(sales.count())
            if sales:
                lastSaleDate = sales.first().date

                for sale in sales:
                    sum = sum + sale.unit_selling_price
                    if sale.date > lastSaleDate:
                        lastSaleDate = sale.date

            array.append({"sales": serializer.data, "total": sum,
                         "lastSaleDate": lastSaleDate, "marginPercent": round(((sum - totalManufacturing) / totalManufacturing)*100, 2) if totalManufacturing != 0 else 0})
        return Response(sorted(array, key=lambda d: d['total'], reverse=True), status=status.HTTP_200_OK)

    def post(self, request):
        '''
        Create an article with the given data
        '''
        data = {
            'code': request.data.get('code'),
            'category': request.data.get('category'),
            'name': request.data.get('name'),
            'manufacturing_cost': request.data.get('manufacturing_cost'),
        }
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
