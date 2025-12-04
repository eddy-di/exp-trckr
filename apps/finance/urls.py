from rest_framework.routers import DefaultRouter
from apps.finance.views.account import AccountViewSet
from apps.finance.views.category import CategoryViewSet
from apps.finance.views.transaction import TransactionViewSet


router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"accounts", AccountViewSet, basename="account")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = router.urls
