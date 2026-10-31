from django.test import TestCase


class PwaTest(TestCase):
    def test_manifest(self):
        response = self.client.get("/manifest.json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["display"], "standalone")

    def test_service_worker(self):
        response = self.client.get("/sw.js")
        self.assertEqual(response.status_code, 200)
        self.assertIn("javascript", response["Content-Type"])
        self.assertIn("caches", response.content.decode())
