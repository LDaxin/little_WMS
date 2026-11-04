from django.contrib.auth.models import User
from django.test import TestCase

from article.models import Article, ArticleBase, ArticleType, Stock


class DetailModalTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_type = ArticleType.objects.create(name="tent", symbol="TZ")
        cls.article = Article.objects.create(
            base=ArticleBase.objects.create(name="Jurte", pType=cls.article_type)
        )
        Stock.objects.create(article=cls.article, stored=None, menge=1)

    def setUp(self):
        User.objects.create_superuser("boss", "b@e.st", "pw")
        self.client.login(username="boss", password="pw")

    def test_detail_returns_a_fragment_for_htmx(self):
        response = self.client.get(
            f"/article/tent/{self.article.pk}", HTTP_HX_REQUEST="true"
        )
        content = response.content.decode()
        self.assertNotIn("<html", content)
        self.assertIn("modalsingle", content)

    def test_direct_url_renders_the_full_page(self):
        response = self.client.get(f"/article/tent/{self.article.pk}")
        self.assertIn("<html", response.content.decode())

    def test_action_urls_are_absolute(self):
        response = self.client.get(
            f"/article/tent/{self.article.pk}", HTTP_HX_REQUEST="true"
        )
        base = f"/article/tent/{self.article.pk}"
        self.assertContains(response, f'action="{base}/update"')
        self.assertContains(response, f'hx-post="{base}/store"')

    def test_list_edit_button_opens_the_modal(self):
        response = self.client.get("/article/tent/search")
        self.assertContains(response, 'hx-target="#modalBodysingle"')

    def test_list_card_opens_the_modal(self):
        response = self.client.get("/article/search", {"mode": "cards"})
        self.assertContains(response, 'hx-target="#modalBodysingle"')
