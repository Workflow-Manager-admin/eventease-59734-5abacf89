from django.contrib import admin
from .models import Venue, Event, Booking, UserProfile

admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(UserProfile)
