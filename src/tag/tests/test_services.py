from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, Stock
from space.models import Space
from tag.models import Tag, TagCategory
from tag.services import effective_tags


def make_article(name, article_type):
    base = ArticleBase.objects.create(name=name, pType=article_type)
    space = Space.objects.create(prefix="a0", active=True)
    return Article.objects.create(base=base, space=space)


class EffectiveTagsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="Werkzeug", symbol="WZ")
        cls.group = TagCategory.objects.create(name="Group", inherit_to_contents=True)
        cls.status = TagCategory.objects.create(name="Status", inherit_to_contents=False)

    def test_own_tags(self):
        article = make_article("Hammer", self.article_type)
        tag = Tag.objects.create(name="Sommer")
        article.tags.add(tag)
        self.assertEqual(effective_tags(article), {tag})

    def test_inherited_tag(self):
        box = make_article("Kiste", self.article_type)
        tag = Tag.objects.create(name="Sommer", category=self.group)
        box.tags.add(tag)
        article = make_article("Hammer", self.article_type)
        Stock.objects.create(article=article, stored=box.space, menge=1)
        self.assertIn(tag, effective_tags(article))

    def test_not_inherited_when_category_off(self):
        box = make_article("Kiste", self.article_type)
        tag = Tag.objects.create(name="defekt", category=self.status)
        box.tags.add(tag)
        article = make_article("Hammer", self.article_type)
        Stock.objects.create(article=article, stored=box.space, menge=1)
        self.assertNotIn(tag, effective_tags(article))

    def test_inherited_tag_disappears_when_removed(self):
        box = make_article("Kiste", self.article_type)
        tag = Tag.objects.create(name="Sommer", category=self.group)
        box.tags.add(tag)
        article = make_article("Hammer", self.article_type)
        stock = Stock.objects.create(article=article, stored=box.space, menge=1)
        self.assertIn(tag, effective_tags(article))
        stock.delete()
        self.assertNotIn(tag, effective_tags(article))
