from django.test import SimpleTestCase

from location.pluscode import encode, decode


class PlusCodeTest(SimpleTestCase):
    # Reference values from the Open Location Code implementation.
    REFERENCE = [
        ((47.365590, 8.524997), "8FVC9G8F+6X"),
        ((40.689167, -74.044444), "87G7MXQ4+M6"),
        ((-33.857, 151.215), "4RRH46V8+62"),
        ((52.5200, 13.4050), "9F4MGCC4+22"),
    ]

    def test_encode_reference_values(self):
        for (lat, lng), expected in self.REFERENCE:
            with self.subTest(lat=lat, lng=lng):
                self.assertEqual(encode(lat, lng), expected)

    def test_decode_reference_values(self):
        for (lat, lng), code in self.REFERENCE:
            with self.subTest(code=code):
                dlat, dlng = decode(code)
                # The decoded point is the centre of the ~14 m cell.
                self.assertAlmostEqual(dlat, lat, places=3)
                self.assertAlmostEqual(dlng, lng, places=3)

    def test_round_trip(self):
        for (lat, lng), _ in self.REFERENCE:
            with self.subTest(lat=lat, lng=lng):
                dlat, dlng = decode(encode(lat, lng))
                self.assertLess(abs(dlat - lat), 0.0002)
                self.assertLess(abs(dlng - lng), 0.0002)

    def test_decode_ignores_separator_and_case(self):
        self.assertEqual(decode("8fvc9g8f+6x"), decode("8FVC9G8F+6X"))

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            encode(91, 0)
        with self.assertRaises(ValueError):
            encode(0, 181)
        with self.assertRaises(ValueError):
            decode("")
