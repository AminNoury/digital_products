from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CategorySerializer, FileSerializer, ProductSerializer
from .models import Category, Product, File


class ProductListView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

