from django.db import models


class RoomRate(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=100)
    default_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.room_name


class OverriddenRoomRate(models.Model):
    room_rate = models.ForeignKey(
        RoomRate, on_delete=models.CASCADE, related_name="overridden_rates"
    )
    stay_date = models.DateField()
    overridden_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.room_rate.room_name} - {self.stay_date}"


class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ("fixed", "Fixed"),
        ("percentage", "Percentage"),
    )

    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.get_discount_type_display()} - {self.discount_value}"


class DiscountRoomRate(models.Model):
    room_rate = models.ForeignKey(
        RoomRate, on_delete=models.CASCADE, related_name="discounts"
    )
    discount = models.ForeignKey(
        Discount, on_delete=models.CASCADE, related_name="room_rates"
    )

    def __str__(self):
        return f"{self.room_rate.room_name} - {self.discount}"
