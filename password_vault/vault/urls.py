from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from vault.views import PasswordEntryListCreate, PasswordEntryDetail, SignupView, LoginView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),  # Login endpoint
    path('logout/', LogoutView.as_view(), name='logout'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('passwords/', PasswordEntryListCreate.as_view(), name='password-list-create'),
    path('passwords/<int:pk>/', PasswordEntryDetail.as_view(), name='password-detail'),
]
