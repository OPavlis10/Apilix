from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ItemViewSet, TagViewSet

router = DefaultRouter()
router.register("items", ItemViewSet, basename="item")
router.register("categories", CategoryViewSet, basename="category")
router.register("tags", TagViewSet, basename="tag")

urlpatterns = router.urls
