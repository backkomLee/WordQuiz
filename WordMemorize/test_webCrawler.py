import unittest
from webCrawler import WebCrawler

class TestSearchEnglish(unittest.TestCase):
   def setUp(self):
      self.w1 = WebCrawler()

   def tearDown(self):
      pass

   def testSearchEnglish(self):
      self.assertEqual(self.w1.searchEnglish('frozen')[0], True)
      self.assertEqual(self.w1.searchEnglish('python')[0], True)
      self.assertEqual(self.w1.searchEnglish('♡♡♡',)[0], False)
      self.assertEqual(self.w1.searchEnglish('kookmin',)[0], True)

if __name__ == '__main__':
   unittest.main()