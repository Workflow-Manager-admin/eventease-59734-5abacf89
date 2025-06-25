from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import Event, Venue, Booking, UserProfile
from .serializers import (
    EventSerializer, VenueSerializer, BookingSerializer,
    UserSerializer, UserProfileSerializer,
)
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def health(request):
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class VenueViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for Venues."""
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# PUBLIC_INTERFACE
class EventViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for Events."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

# PUBLIC_INTERFACE
class BookingViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for Booking (event registration)."""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow a user to see their own bookings, or all if staff
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# PUBLIC_INTERFACE
class RegisterView(APIView):
    """Endpoint for user registration."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        if not username or not email or not password:
            return Response({"error": "Required fields missing"}, status=400)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username taken"}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        return Response({"message": "User created!"}, status=201)

# PUBLIC_INTERFACE
class LoginView(ObtainAuthToken):
    """Endpoint for user login, returns token."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username,
        })

# PUBLIC_INTERFACE
class ProfileView(APIView):
    """Endpoint to get/update user profile."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        return Response(UserProfileSerializer(profile).data)

    def put(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# PUBLIC_INTERFACE
class UserEventsView(APIView):
    """Get events the user is registered for."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        events = [booking.event for booking in bookings]
        return Response(EventSerializer(events, many=True).data)
