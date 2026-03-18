from django.db import models
from vehicles.models import Vehicle

class MaintenanceRecord(models.Model):
    SERVICE_CHOICES = [
        ('oil_change', 'Oil Change'),
        ('service', 'Service'),
        ('tire_replacement', 'Tire Replacement'),
        ('custom', 'Custom Maintenance'),
    ]

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records')
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    next_service_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.vehicle.name} on {self.date}"

    class Meta:
        ordering = ['-date']
