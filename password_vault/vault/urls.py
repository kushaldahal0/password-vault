from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from vault.views import PasswordEntryListCreate, PasswordEntryDetail

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('passwords/', PasswordEntryListCreate.as_view(), name='password-list-create'),
    path('passwords/<int:pk>/', PasswordEntryDetail.as_view(), name='password-detail'),
]
