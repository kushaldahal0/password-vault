from rest_framework import serializers
from .models import PasswordEntry
from cryptography.fernet import Fernet
from django.conf import settings
import hashlib
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class PasswordEntrySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Make user read-only

    class Meta:
        model = PasswordEntry
        fields = ['id', 'user', 'url', 'username', 'password', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']  # Ensure 'user' is read-only

    def create(self, validated_data):
        user = self.context['request'].user  # Get the user from the request context
        plaintext_password = validated_data.pop('password')

        # Generate password hash
        password_hash = hashlib.sha256(plaintext_password.encode()).hexdigest()

        # Check for duplicates
        if PasswordEntry.objects.filter(
            user=user,
            url=validated_data['url'],
            username=validated_data['username'],
            password_hash=password_hash
        ).exists():
            raise serializers.ValidationError("This entry already exists.")

        # Encrypt password
        cipher_suite = Fernet(settings.FERNET_KEY)
        encrypted_password = cipher_suite.encrypt(plaintext_password.encode())

        # Create the PasswordEntry with the authenticated user
        return PasswordEntry.objects.create(
            user=user,  # Assign the user
            encrypted_password=encrypted_password,  # BinaryField stores bytes
            password_hash=password_hash,
            **validated_data
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        cipher_suite = Fernet(settings.FERNET_KEY)

        # Ensure encrypted_password is in bytes before decrypting
        if isinstance(instance.encrypted_password, memoryview):
            encrypted_password = bytes(instance.encrypted_password)
        else:
            encrypted_password = instance.encrypted_password

        data['password'] = cipher_suite.decrypt(encrypted_password).decode()
        return data
