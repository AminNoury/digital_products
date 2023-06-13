import uuid
from datetime import timedelta
from django.utils import timezone



from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import GatewaySerializer
from .models import Gateway, Payment
from subscriptions.models import Package, Subscription


class GatewayView(APIView):
    def get(self, request):
        gateways = Gateway.objects.filter(is_enable=True)
        serializer = GatewaySerializer(gateways, many=True)
        return Response(serializer.data)

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        gateway_id = request.query_param.get('gateway')
        package_id = request.query_param.get('package')

        try:
            gateway = Gateway.objects.get(pk=gateway_id, is_enable=True)
            package = Package.objects.get(pk=package_id, is_enable=True)
        except (Gateway.DoesNotExist, Package.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            user=request.user,
            package=package,
            price=package.price,
            phone_number=request.user.phone_number,
            token=str(uuid.uuid4())
        )

        return Response({'token': payment.token, 'callback_url': 'http//:my_site.com/payments/pay'})
    def post(self, request):
        token = request.data.get('token')
        st = request.data.get('status')

        try:
            payment = Payment.objects.filter(token=token)
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if st != 10:
            payment.status = payment.STATUS_CANCELED
            payment.save()
            return Response({'detail': 'payment canceled by user'}, status=status.HTTP_400_BAD_REQUEST)

        r = request.post('bank-verify_url', data={})
        if r.status_code // 100 != 2:
            payment.status = Payment.STATUS_ERROR
            payment.save()
            return Response({'detail': 'payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)

        payment.status = Payment.STATUS_PAID
        payment.save()

        Subscription.objects.create(
            user=payment.user,
            package=payment.package,
            expire_time=timezone.now()+timezone.timedelta(days=payment.package.duration.days)
        )

        return Response({'detail': 'payment is successful'})



