from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max
from datetime import datetime, timedelta
from .models import RoomRate, OverriddenRoomRate, DiscountRoomRate, Discount
from .serializers import (
    RoomRateSerializer,
    OverriddenRoomRateSerializer,
    DiscountSerializer,
    DiscountRoomRateSerializer,
)


class RoomRateViewSet(viewsets.ModelViewSet):
    queryset = RoomRate.objects.all()
    serializer_class = RoomRateSerializer


class OverriddenRoomRateViewSet(viewsets.ModelViewSet):
    queryset = OverriddenRoomRate.objects.all()
    serializer_class = OverriddenRoomRateSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class DiscountRoomRateViewSet(viewsets.ModelViewSet):
    queryset = DiscountRoomRate.objects.all()
    serializer_class = DiscountRoomRateSerializer


class FinalRateView(APIView):
    def get(self, request):
        # Extract query parameters
        room_id = request.query_params.get("room_id")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # Validate mandatory parameters
        if not room_id or not start_date or not end_date:
            return Response(
                {
                    "error": "room_id, start_date, and end_date are mandatory parameters."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to fetch the RoomRate object
        try:
            room_rate = RoomRate.objects.get(room_id=room_id)
        except RoomRate.DoesNotExist:
            return Response(
                {"error": "Room rate not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Convert start_date and end_date from string to date objects
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure start_date is before or equal to end_date
        if start_date > end_date:
            return Response(
                {"error": "start_date must be before or equal to end_date."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_date = start_date
        final_rates = []

        while current_date <= end_date:
            # Check for overridden rates
            overridden_rates = OverriddenRoomRate.objects.filter(
                room_rate=room_rate, stay_date=current_date
            )
            if overridden_rates.exists():
                overridden_rate = (
                    overridden_rates.first().overridden_rate
                )  # Take the first if multiple exist
            else:
                overridden_rate = room_rate.default_rate

            # Find the highest discount
            discounts = DiscountRoomRate.objects.filter(room_rate=room_rate)
            highest_discount_value = 0
            for discount in discounts:
                if discount.discount.discount_type == "fixed":
                    highest_discount_value = max(
                        highest_discount_value, discount.discount.discount_value
                    )
                elif discount.discount.discount_type == "percentage":
                    highest_discount_value = max(
                        highest_discount_value,
                        overridden_rate * (discount.discount.discount_value / 100),
                    )

            final_rate = max(
                0, overridden_rate - highest_discount_value
            )  # Ensure the final rate is not negative

            final_rates.append(
                {
                    "room_id": room_rate.room_id,
                    "room_name": room_rate.room_name,
                    "date": current_date,
                    "final_rate": final_rate,
                }
            )
            current_date += timedelta(days=1)

        return Response(final_rates, status=status.HTTP_200_OK)
