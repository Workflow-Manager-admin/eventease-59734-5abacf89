from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Venue, Booking, UserProfile

# PUBLIC_INTERFACE
class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django's User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# PUBLIC_INTERFACE
class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile paired with the Django User."""
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['user', 'phone', 'bio']

# PUBLIC_INTERFACE
class VenueSerializer(serializers.ModelSerializer):
    """Serializer for Venue model."""
    class Meta:
        model = Venue
        fields = '__all__'

# PUBLIC_INTERFACE
class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""
    organizer = UserSerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    venue_id = serializers.PrimaryKeyRelatedField(
        queryset=Venue.objects.all(), source='venue', write_only=True
    )

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_datetime', 'end_datetime',
            'venue', 'venue_id', 'organizer', 'max_participants'
        ]

# PUBLIC_INTERFACE
class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model."""
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), source='event', write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'user', 'event', 'event_id', 'booking_datetime']
