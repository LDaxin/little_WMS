"""Read-only API viewsets (§7a)."""
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (
    ArticleBaseSerializer,
    ArticleSerializer,
    ArticleTypeSerializer,
    LocationSerializer,
    NotificationSerializer,
    OccasionSerializer,
    SpaceSerializer,
    StorageSerializer,
    StorageTypeSerializer,
    TagSerializer,
)
from article.models import Article, ArticleBase, ArticleType
from location.models import Location
from notifications.models import Notification
from occasion.models import Occasion
from space.models import Space
from storage.models import Storage, StorageType
from tag.models import Tag


class ArticleViewSet(ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_area = "article"


class ArticleBaseViewSet(ReadOnlyModelViewSet):
    queryset = ArticleBase.objects.all()
    serializer_class = ArticleBaseSerializer
    permission_area = "article"


class ArticleTypeViewSet(ModelViewSet):
    queryset = ArticleType.objects.all()
    serializer_class = ArticleTypeSerializer
    permission_area = "article"


class StorageViewSet(ReadOnlyModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_area = "storage"


class StorageTypeViewSet(ModelViewSet):
    queryset = StorageType.objects.all()
    serializer_class = StorageTypeSerializer
    permission_area = "storage"


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_area = "location"


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_area = "tag"


class SpaceViewSet(ReadOnlyModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_area = "storage"


class OccasionViewSet(ReadOnlyModelViewSet):
    queryset = Occasion.objects.all()
    serializer_class = OccasionSerializer
    permission_area = "occasion"


class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_area = "notification"

    def get_queryset(self):
        return self.request.user.notifications.all()
