from django.core.management.base import BaseCommand

from article.models import Article, ArticleBase, ArticleType, Stock
from space.models import Space
from storage.models import Storage, StorageType


class Command(BaseCommand):
    help = "Create N test articles with stocks, to exercise the list views."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=60)
        parser.add_argument("--type", default="test")

    def handle(self, *args, **options):
        count = options["count"]
        article_type, _ = ArticleType.objects.get_or_create(
            name=options["type"], defaults={"symbol": "TS"}
        )
        storage_type, _ = StorageType.objects.get_or_create(
            name="testroom", defaults={"symbol": "TR"}
        )
        storage, _ = Storage.objects.get_or_create(
            name="Testregal", defaults={"typ": storage_type}
        )

        created = 0
        for i in range(1, count + 1):
            base, _ = ArticleBase.objects.get_or_create(
                name="Testartikel %03d" % i, pType=article_type
            )
            article, was_created = Article.objects.get_or_create(base=base)
            if was_created:
                space = Space.objects.create(prefix="a0", active=False)
                article.space = space
                article.save()
                Stock.objects.create(article=article, stored=storage.space, menge=1)
                created += 1

        self.stdout.write(self.style.SUCCESS("Created %d test articles." % created))
