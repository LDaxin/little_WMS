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
            f"/article/tent/{self.article.pk}/i", HTTP_HX_REQUEST="true"
        )
        base = f"/article/tent/{self.article.pk}"
        self.assertContains(response, f'action="{base}/update"')
        self.assertContains(response, f'hx-post="{base}/update"')

    def test_list_edit_button_opens_the_modal(self):
        response = self.client.get("/article/tent/search")
        self.assertContains(response, 'hx-target="#modalBodysingle"')

    def test_list_card_opens_the_modal(self):
        response = self.client.get("/article/search", {"mode": "cards"})
        self.assertContains(response, 'hx-target="#modalBodysingle"')


class DetailViewTest(TestCase):
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

    def test_detail_has_compact_header_and_edit(self):
        response = self.client.get(f"/article/tent/{self.article.pk}")
        self.assertContains(response, "detailHeader")
        self.assertContains(response, f'hx-get="/article/tent/{self.article.pk}/i"')

    def test_detail_is_read_only_by_default(self):
        response = self.client.get(f"/article/tent/{self.article.pk}")
        content = response.content.decode()
        self.assertIn('id="detailFields"', content)
        self.assertNotIn("<form", content.split('id="detailFields"')[1].split("detailSections")[0])

    def test_sections_are_collapsed_details(self):
        response = self.client.get(f"/article/tent/{self.article.pk}")
        self.assertContains(response, '<details id="section-tags"')

    def test_edit_fragment_returns_the_form(self):
        response = self.client.get(f"/article/tent/{self.article.pk}/i")
        content = response.content.decode()
        self.assertIn('id="detailFields"', content)
        self.assertIn("<form", content)
        self.assertIn("Cancel", content)

    def test_read_fragment_returns_the_summary(self):
        response = self.client.get(f"/article/tent/{self.article.pk}?fields=read")
        content = response.content.decode()
        self.assertIn('id="detailFields"', content)
        self.assertNotIn("<form", content)

    def test_layout_defaults_to_accordion(self):
        response = self.client.get(f"/article/tent/{self.article.pk}")
        self.assertContains(response, '<details id="section-tags"')

    def test_layout_parameter_wins(self):
        response = self.client.get(f"/article/tent/{self.article.pk}?layout=tabs")
        content = response.content.decode()
        self.assertIn('data-bs-target="#section-tags"', content)
        self.assertNotIn('<details id="section-tags"', content)

    def test_mobile_forces_accordion_and_hides_toggle(self):
        response = self.client.get(
            f"/article/tent/{self.article.pk}?layout=tabs", HTTP_X_VIEW_MODE="mobile"
        )
        content = response.content.decode()
        self.assertIn('<details id="section-tags"', content)
        self.assertNotIn("fields=sections", content)

    def test_edit_form_uses_the_update_prefixes(self):
        response = self.client.get(f"/article/tent/{self.article.pk}/i", HTTP_HX_REQUEST="true")
        self.assertContains(response, 'name="base-name"')
        self.assertContains(response, 'name="article-zustand"')

    def test_edit_form_round_trip_saves(self):
        self.client.post(
            f"/article/tent/{self.article.pk}/update",
            {
                "base-name": "Jurte",
                "article-zustand": "defekt",
                "version": str(self.article.version),
            },
            HTTP_HX_REQUEST="true",
        )
        self.article.refresh_from_db()
        self.assertEqual(self.article.zustand, "defekt")
