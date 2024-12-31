from rest_framework.routers import DefaultRouter
from .views import ElementViewSet

router = DefaultRouter()
router.register(r'elements',ElementViewSet,basename='elements')

urlpatterns = router.urls
