from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from server.apps.payments.enums import PaymentStatuses
from server.apps.payments.helpers import verify_signature
from server.apps.payments.models import Payment


@api_view(['POST'])
def process_payment(request):
    """Вебхук обработки результата платежа."""
    data = dict(request.data)
    print(data)
    products = {
        'name': data.pop('products[0][name]')[0],
        'price': data.pop('products[0][price]')[0],
        'quantity': data.pop('products[0][quantity]')[0],
        'sum': data.pop('products[0][sum]')[0],
    }
    data = {key: value[0] for key, value in data.items()}
    data['products'] = [products]
    sign = request.headers.get('Sign')
    verified = verify_signature(data, sign)
    if verified == 'false':
        raise AuthenticationFailed()

    if data.get('customer_extra'):
        payment = Payment.objects.filter(pk=data.get('customer_extra')).first()
        if payment:
            if payment.status == PaymentStatuses.NEW:
                payment.data = data
                payment_status = data.get('payment_status')

                if payment_status == 'success':
                    payment.status = PaymentStatuses.SUCCESS
                else:
                    payment.status = PaymentStatuses.FAIL
                payment.save(update_fields=['data', 'status'])

    return Response(status=status.HTTP_200_OK)
