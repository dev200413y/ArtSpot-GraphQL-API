from django.db import models


class Shop(models.Model):
    """
    Shop model with:
      - name    : CharField
      - email   : JSONField (stores list of email strings)
      - phone   : JSONField (stores list of phone strings)
      - address : TextField
    """
    name       = models.CharField(max_length=255)
    email      = models.JSONField(default=list)   # Array of email addresses
    phone      = models.JSONField(default=list)   # Array of phone numbers
    address    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
