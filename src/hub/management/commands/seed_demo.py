from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from article.models import Article, ArticleBase, ArticleType
from space.models import Space
from storage.models import Storage, StorageType
from tag.models import Tag


# name, symbol, article_toggle_space
ARTICLE_TYPES = [
    ("tent", "TZ", True),
    ("tool", "WZ", False),
    ("kitchen", "KU", False),
]

ARTICLES = {
    "tent": ["Jurte 8P", "Kuppelzelt 4P", "Tarp 3x3", "Schlafsack", "Isomatte", "Zeltplane", "Heringe"],
    "tool": ["Hammer", "Zange", "Saege", "Axt", "Schraubenschluessel", "Beil", "Werkzeugkiste"],
    "kitchen": ["Kochtopf", "Pfanne", "Gaskocher", "Kiste Besteck", "Kelle", "Geschirrset"],
}

# name, symbol
STORAGE_TYPES = [
    ("building", "GE"),
    ("room", "RA"),
    ("shelf", "RE"),
    ("compartment", "FA"),
]

# name, type, parent
STORAGES = [
    ("Vereinsheim", "building", None),
    ("Lagerraum", "room", "Vereinsheim"),
    ("Regal 1", "shelf", "Lagerraum"),
    ("Fach A", "compartment", "Regal 1"),
    ("Fach B", "compartment", "Regal 1"),
]

TAGS = ["Sommer", "Winter", "Zeltlager"]


class Command(BaseCommand):
    help = "Create a small realistic demo dataset (idempotent)."

    def handle(self, *args, **options):
        self._user()
        article_types = self._article_types()
        storages = self._storage_types_and_storages()
        self._tags()
        self._articles(article_types, storages)

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
        self.stdout.write(
            "  ArticleType %d  ArticleBase %d  Article %d"
            % (ArticleType.objects.count(), ArticleBase.objects.count(), Article.objects.count())
        )
        self.stdout.write(
            "  StorageType %d  Storage %d  Tag %d"
            % (StorageType.objects.count(), Storage.objects.count(), Tag.objects.count())
        )

    def _user(self):
        user, created = User.objects.get_or_create(username="demo")
        if created:
            user.set_password("demo")
            user.save()

    def _article_types(self):
        types = {}
        for name, symbol, toggle in ARTICLE_TYPES:
            types[name], _ = ArticleType.objects.get_or_create(
                name=name, defaults={"symbol": symbol, "article_toggle_space": toggle}
            )
        return types

    def _storage_types_and_storages(self):
        types = {}
        for name, symbol in STORAGE_TYPES:
            types[name], _ = StorageType.objects.get_or_create(
                name=name, defaults={"symbol": symbol}
            )
        storages = {}
        for name, type_name, parent_name in STORAGES:
            storages[name], _ = Storage.objects.get_or_create(
                name=name,
                defaults={"typ": types[type_name], "parent": storages.get(parent_name)},
            )
        return storages

    def _tags(self):
        for name in TAGS:
            Tag.objects.get_or_create(name=name)

    def _articles(self, article_types, storages):
        targets = [storages["Fach A"], storages["Fach B"]]
        index = 0
        for type_name, names in ARTICLES.items():
            article_type = article_types[type_name]
            for name in names:
                base, _ = ArticleBase.objects.get_or_create(name=name, pType=article_type)
                article, created = Article.objects.get_or_create(base=base)
                if created:
                    space = Space.objects.create(
                        prefix="a0", active=article_type.article_toggle_space
                    )
                    article.space = space
                    article.stored = targets[index % len(targets)].space
                    article.save()
                index += 1
