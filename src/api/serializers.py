"""DRF serializers (§7a)."""
from rest_framework import serializers

from article.models import Article, ArticleBase, ArticleType
from location.models import Location
from notifications.models import Notification
from occasion.models import Occasion
from space.models import Space
from storage.models import Storage, StorageType
from tag.models import Tag


class ArticleSerializer(serializers.ModelSerializer):
    # Derived from the open loan (RF-004), so read-only.
    ownership = serializers.CharField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleBase
        fields = "__all__"


class ArticleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleType
        fields = "__all__"
        read_only_fields = ["code", "organisation"]


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = "__all__"


class StorageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageType
        fields = "__all__"
        read_only_fields = ["code", "organisation"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        read_only_fields = ["code", "organisation"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ["code", "organisation"]


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = "__all__"


class OccasionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
