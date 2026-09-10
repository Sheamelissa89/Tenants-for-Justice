from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Case(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("resolved", "Resolved"), ("archived", "Archived")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="housing_cases")
    title = models.CharField(max_length=160)
    property_address = models.CharField(max_length=255)
    landlord_or_manager = models.CharField(max_length=160, blank=True)
    move_in_date = models.DateField(blank=True, null=True)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("case_detail", kwargs={"pk": self.pk})


class Incident(models.Model):
    CATEGORY_CHOICES = [("repair", "Repair or maintenance"), ("communication", "Communication"), ("inspection", "Inspection or entry"), ("notice", "Notice received or sent"), ("payment", "Rent or payment"), ("other", "Other")]
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="incidents")
    title = models.CharField(max_length=160)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    occurred_at = models.DateTimeField()
    description = models.TextField()
    people_involved = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_at"]

    def __str__(self):
        return self.title


class Evidence(models.Model):
    TYPE_CHOICES = [("photo", "Photo"), ("video", "Video"), ("audio", "Audio"), ("message", "Message or email"), ("notice", "Notice or letter"), ("report", "Inspection or contractor report"), ("receipt", "Receipt or payment record"), ("other", "Other")]
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name="evidence")
    incident = models.ForeignKey(Incident, on_delete=models.SET_NULL, related_name="evidence", blank=True, null=True)
    title = models.CharField(max_length=160)
    evidence_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    file = models.FileField(upload_to="evidence/%Y/%m/")
    notes = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title

# Create your models here.
