from rest_framework import serializers

from .models import Gateway, Payment


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ('id', 'title', 'description', 'avatar')


