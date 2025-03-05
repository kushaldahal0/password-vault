from django.db import models
from django.contrib.auth import get_user_model
import hashlib

User = get_user_model()

class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    username = models.CharField(max_length=255)
    encrypted_password = models.BinaryField()
    password_hash = models.CharField(max_length=64)  # SHA256
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'url', 'username', 'password_hash'],
                name='unique_password_entry'
            )
        ]

    def __str__(self):
        return f"{self.url} - {self.username}"