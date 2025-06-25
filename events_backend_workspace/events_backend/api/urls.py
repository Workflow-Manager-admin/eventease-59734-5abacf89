from django.urls import path, include
from .views import (
    health, RegisterView, LoginView, ProfileView, UserEventsView,
    VenueViewSet, EventViewSet, BookingViewSet
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'venues', VenueViewSet, basename='venue')
router.register(r'events', EventViewSet, basename='event')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('health/', health, name='Health'),
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my-events/', UserEventsView.as_view(), name='user-events'),
    path('', include(router.urls)),
]
