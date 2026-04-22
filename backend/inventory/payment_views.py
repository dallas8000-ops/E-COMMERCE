from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class FlutterwavePaymentInit(APIView):
    """
    Initiate a payment via Flutterwave (handles M-Pesa, Airtel, MTN, cards, etc.)
    This is a stub. Integrate with Flutterwave API and add authentication as needed.
    """
    def post(self, request):
        # Example: Accept amount, currency, customer info, etc.
        data = request.data
        # Here you would call the payments microservice or Flutterwave API
        return Response({
            'message': 'Flutterwave payment initiation endpoint. Integrate with Flutterwave API here.',
            'data_received': data
        }, status=status.HTTP_200_OK)
