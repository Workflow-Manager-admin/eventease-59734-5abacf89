from django.db import models
from django.contrib.auth.models import User

# PUBLIC_INTERFACE
class Venue(models.Model):
    """A venue where events are held."""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512)
    city = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# PUBLIC_INTERFACE
class UserProfile(models.Model):
    """Profile details for event users."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

# PUBLIC_INTERFACE
class Event(models.Model):
    """An individual event."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    max_participants = models.PositiveIntegerField()

    def __str__(self):
        return self.title

# PUBLIC_INTERFACE
class Booking(models.Model):
    """A user's registration (booking) for an event."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    booking_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} booking for {self.event.title}"
