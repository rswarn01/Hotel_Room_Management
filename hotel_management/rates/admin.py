from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(RoomRate)
admin.site.register(Discount)
admin.site.register(DiscountRoomRate)
admin.site.register(OverriddenRoomRate)
