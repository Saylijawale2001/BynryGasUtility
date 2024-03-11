from django.db import models
from django.contrib.auth.models import User

class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('InProgress', 'In Progress'),
        ('Completed', 'Completed'),
    )

    REQUEST_TYPE_CHOICES = (
        ('Connection', 'New Connection'),
        ('Disconnection', 'Disconnection'),
        ('Leak', 'Gas Leak'),
        ('Meter', 'Meter Replacement/Repair'),
        ('Billing', 'Billing Inquiry'),
        ('Others', 'Other Issues'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=100, choices=REQUEST_TYPE_CHOICES)
    details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submission_date = models.DateTimeField(auto_now_add=True)
    resolution_date = models.DateTimeField(null=True, blank=True)
    attachment = models.FileField(upload_to='service_request_attachments/', null=True, blank=True)

    def __str__(self):
        return f"{self.request_type} - {self.status}"

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    meter_number = models.CharField(max_length=50)
    billing_information = models.TextField()
    contact_number = models.CharField(max_length=20)
    emergency_contact_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
