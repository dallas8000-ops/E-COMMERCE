from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class PaymentCheckoutStub(APIView):
    """
    Placeholder for a future card/mobile-money gateway.
    The live storefront completes orders via checkout + manual payment verification (MTN, Airtel, WorldRemit, etc.).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        return Response(
            {
                'message': (
                    'No third-party gateway is configured. Complete payment using the instructions '
                    'shown at checkout; staff confirms receipt in Django admin.'
                ),
                'data_received': data,
            },
            status=status.HTTP_200_OK,
        )
