import unittest
from URL import URL
from Exceptions import *

class URLTest(unittest.TestCase):
    def test_vaild_url(self):
        url = URL("https://www.google.com/")
        self.assertEqual(url.link,"https://www.google.com/")

    def test_invaild_url(self):
        self.assertRaises(InvaildURL,URL,"google")

if __name__ == "__main__":
    unittest.main()