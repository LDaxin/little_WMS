from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register("articles", views.ArticleViewSet)
router.register("article-bases", views.ArticleBaseViewSet)
router.register("article-types", views.ArticleTypeViewSet)
router.register("storages", views.StorageViewSet)
router.register("storage-types", views.StorageTypeViewSet)
router.register("locations", views.LocationViewSet)
router.register("tags", views.TagViewSet)
router.register("spaces", views.SpaceViewSet)
router.register("occasions", views.OccasionViewSet)
router.register("notifications", views.NotificationViewSet, basename="notification")

urlpatterns = router.urls
