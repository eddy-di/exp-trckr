from rest_framework.routers import DefaultRouter
from apps.finance.views.category import CategoryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")

urlpatterns = router.urls
