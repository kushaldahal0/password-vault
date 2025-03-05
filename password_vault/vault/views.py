from rest_framework import generics, permissions
from .models import PasswordEntry
from .serializers import PasswordEntrySerializer

class PasswordEntryListCreate(generics.ListCreateAPIView):
    serializer_class = PasswordEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PasswordEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class PasswordEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PasswordEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PasswordEntry.objects.filter(user=self.request.user)