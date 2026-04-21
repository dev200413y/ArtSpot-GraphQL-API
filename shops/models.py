from django.db import models


class Shop(models.Model):
    """
    Represents a shop entity.

    Fields:
        name    - Shop name (string)
        email   - List of email addresses (stored as JSON array)
        phone   - List of phone numbers (stored as JSON array)
        address - Physical address of the shop
    """
    name = models.CharField(max_length=255)
    email = models.JSONField(
        default=list,
        help_text="Array of email addresses associated with the shop."
    )
    phone = models.JSONField(
        default=list,
        help_text="Array of phone numbers associated with the shop."
    )
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
