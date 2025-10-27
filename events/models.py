from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class EventCategory(models.Model):
    """Categories for campus events (e.g., Academic, Sports, Cultural, etc.)"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Event Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    """Model for campus events"""

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    category = models.ForeignKey(
        EventCategory, on_delete=models.SET_NULL, null=True, related_name="events"
    )
    organizer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="organized_events"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    max_participants = models.PositiveIntegerField(
        null=True, blank=True, help_text="Leave blank for unlimited participants"
    )
    registration_required = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_datetime"]
        indexes = [
            models.Index(fields=["start_datetime", "status"]),
            models.Index(fields=["category", "status"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%Y-%m-%d')}"

    @property
    def is_upcoming(self):
        """Check if event is in the future"""
        return self.start_datetime > timezone.now()

    @property
    def is_ongoing(self):
        """Check if event is currently happening"""
        now = timezone.now()
        return self.start_datetime <= now <= self.end_datetime

    @property
    def is_past(self):
        """Check if event has ended"""
        return self.end_datetime < timezone.now()


class EventRegistration(models.Model):
    """Track user registrations for events"""

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="registrations"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_registrations"
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ["event", "user"]
        ordering = ["-registered_at"]

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
