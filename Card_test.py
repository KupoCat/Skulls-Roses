from Card import Card
import unittest
class CardTest(unittest.TestCase):
    def setUp(self):
        self.skull_card = Card(isSkull=True)
        self.rose_card = Card(isSkull=False)
    
    def test_skull(self):
        self.assertTrue(self.skull_card.isSkull)
    
    def test_rose(self):
        self.assertFalse(self.rose_card.isSkull)