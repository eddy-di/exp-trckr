from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.users.views import MultiFieldTokenObtainPairView, RegisterAPIView


urlpatterns = [
    # ✅ AUTH
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("token/", MultiFieldTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
