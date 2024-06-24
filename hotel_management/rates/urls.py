from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoomRateViewSet,
    OverriddenRoomRateViewSet,
    DiscountViewSet,
    DiscountRoomRateViewSet,
    FinalRateView,
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r"room-rates", RoomRateViewSet)
router.register(r"overridden-rates", OverriddenRoomRateViewSet)
router.register(r"discounts", DiscountViewSet)
router.register(r"discount-room-rates", DiscountRoomRateViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Include the router URLs
    path("final-rate/", FinalRateView.as_view(), name="final-rate"),
]
