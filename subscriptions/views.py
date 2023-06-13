from datetime import timedelta

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import Package, Subscription
from .serializers import PackageSerializer, SubscriptionSerializer

class PackageView(APIView):
    def get(self,request):
        package = Package.objects.filter(is_enable=True)
        serializer = PackageSerializer(package, many=True)
        return Response(serializer.data)

class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        subscriptions = Subscription.objects.filter(
            user=request.user,
            expire_time__gt=timezone.now()
        )

        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)