from rest_framework import serializers

from .models import Package, Subscription


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ('id', 'title', 'sku', 'description', 'avatar', 'price', 'duration', 'create_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    class Meta:
        model = Subscription
        fields = ('package', 'create_time', 'expire_time')