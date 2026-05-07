from django.db import models


class StaffPortalConfig(models.Model):
    """Defines custom permissions for the storefront staff dashboard (no data rows required)."""

    class Meta:
        verbose_name = 'Staff portal'
        verbose_name_plural = 'Staff portal'
        permissions = [
            ('access_staff_dashboard', 'Can access staff dashboard'),
        ]

    def __str__(self):
        return 'Staff portal'

