from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from article.models import Article, ArticleBase, ArticleType, Stock
from location.models import Location
from occasion.models import Occasion, OccasionTemplate, OccasionType, Packlist
from planning.models import CalendarEntry
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

# line1, city, country
LOCATIONS = [
    ("Musterstrasse 1", "Musterstadt", "DE"),
    ("Am See 5", "Waldsee", "DE"),
]

# name, symbol
OCCASION_TYPES = [
    ("Camp", "LA"),
    ("Trip", "FA"),
]

# title, type, location, start, end, participants, packlist [(article, qty)]
OCCASIONS = [
    ("Sommerlager 2026", "Camp", "Am See 5", "2026-07-01", "2026-07-14", 30,
     [("Jurte 8P", 4), ("Kuppelzelt 4P", 2), ("Schlafsack", 20)]),
    ("Herbstfahrt 2026", "Trip", None, "2026-10-10", None, 12,
     [("Kuppelzelt 4P", 2)]),
]

# name, type, default packlist [(article, qty)]
OCCASION_TEMPLATES = [
    ("Standard Sommerlager", "Camp",
     [("Jurte 8P", 4), ("Kuppelzelt 4P", 2), ("Schlafsack", 20)]),
]


class Command(BaseCommand):
    help = "Create a small realistic demo dataset (idempotent)."

    def handle(self, *args, **options):
        self._user()
        article_types = self._article_types()
        storages = self._storage_types_and_storages()
        self._tags()
        articles = self._articles(article_types, storages)
        locations = self._locations()
        occasion_types = self._occasion_types()
        self._occasions(occasion_types, locations, articles)
        self._occasion_templates(occasion_types, articles)

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
        self.stdout.write(
            "  ArticleType %d  ArticleBase %d  Article %d"
            % (ArticleType.objects.count(), ArticleBase.objects.count(), Article.objects.count())
        )
        self.stdout.write(
            "  StorageType %d  Storage %d  Tag %d  Location %d"
            % (StorageType.objects.count(), Storage.objects.count(), Tag.objects.count(), Location.objects.count())
        )
        self.stdout.write(
            "  OccasionType %d  Occasion %d  OccasionTemplate %d"
            % (OccasionType.objects.count(), Occasion.objects.count(), OccasionTemplate.objects.count())
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
        articles = {}
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
                    article.save()
                    Stock.objects.create(
                        article=article,
                        stored=targets[index % len(targets)].space,
                        menge=1,
                    )
                articles[name] = article
                index += 1
        return articles

    def _locations(self):
        locations = {}
        for line1, city, country in LOCATIONS:
            locations[line1], _ = Location.objects.get_or_create(
                line1=line1, defaults={"city": city, "country": country}
            )
        return locations

    def _occasion_types(self):
        types = {}
        for name, symbol in OCCASION_TYPES:
            types[name], _ = OccasionType.objects.get_or_create(
                name=name, defaults={"symbol": symbol}
            )
        return types

    def _occasions(self, occasion_types, locations, articles):
        for title, type_name, location_name, start, end, participants, packlist in OCCASIONS:
            entry, _ = CalendarEntry.objects.get_or_create(
                title=title,
                defaults={"entry_type": "occasion", "start_date": start, "end_date": end},
            )
            occasion, _ = Occasion.objects.get_or_create(
                calendar_entry=entry,
                defaults={
                    "occasion_type": occasion_types[type_name],
                    "location": locations.get(location_name),
                    "participant_count": participants,
                },
            )
            for article_name, quantity in packlist:
                Packlist.objects.get_or_create(
                    occasion=occasion,
                    article=articles[article_name],
                    defaults={"quantity": quantity},
                )

    def _occasion_templates(self, occasion_types, articles):
        for name, type_name, packlist in OCCASION_TEMPLATES:
            OccasionTemplate.objects.get_or_create(
                name=name,
                defaults={
                    "occasion_type": occasion_types[type_name],
                    "default_packlist": [
                        {"article": articles[article_name].pk, "quantity": quantity}
                        for article_name, quantity in packlist
                    ],
                },
            )
