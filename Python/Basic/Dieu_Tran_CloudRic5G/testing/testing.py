from unittest import TestCase, main
from sys import path
path.append('../')
from card import Card, CardCreate
from card_game import CardGame, Player, TheHouse
class TestCardClass(TestCase):
    def test_greater(self):
        testpobj1 = Card('a', 1)
        testobj2 = Card('b', 2)
        # print(f'input:\n===Card1==={testpobj1}\n====Card2==={testobj2}')
        self.assertTrue(testobj2>testpobj1)
    
    def test_less(self):
        testobj1 = Card('a', 1)
        testobj2 = Card('b', 2)
        # print(f'input:\n===Card1==={testobj1}\n====Card2==={testobj2}')
        self.assertTrue(testobj1<testobj2)
    
    def test_equal(self):
        testobj1 = Card('a', 1)
        testobj2 = Card('b', 1)
        # print(f'input:\n===Card1==={testobj1}\n====Card2==={testobj2}')
        self.assertTrue(testobj2==testobj1)

class TestCardBuilderClass(TestCase):
    def test_normal_card_true(self):
        testobj = CardCreate().__call__('H-2')
        self.assertEqual(testobj.name,'H-2')
        self.assertEqual(testobj.point,13*4+2)
    def test_greatest_card_true(self):
        testobj = CardCreate().__call__('Bj')
        self.assertEqual(testobj.name,'BJ')
        self.assertEqual(testobj.point,100)
        
    def test_valid_card_name0_false(self):
        with self.assertRaises(ValueError):
            CardCreate().__call__('A-2')
    def test_valid_card_name1_false(self):
        with self.assertRaises(ValueError):
            CardCreate().__call__('A-2-3')
    def test_valid_card_name2_false(self):
        with self.assertRaises(ValueError):
            CardCreate().__call__('A 2 3')
    def test_card_name_nothing_false(self):
        with self.assertRaises(ValueError):
            CardCreate().__call__('')
    def test_card_name_number_false(self):
        with self.assertRaises(ValueError):
            CardCreate().__call__(4)

class TestCardGameClass(TestCase):
    def test_card_game_property_true(self):
        testobj = CardGame(Player(), TheHouse())
        self.assertIsInstance(testobj.player, Player) 
        self.assertIsInstance(testobj.the_house, TheHouse)
        testobj.reward = 1000
        self.assertTrue(testobj.iswin)
        testobj.player.point = 20
        self.assertTrue(testobj.islose)
    
    def test_card_game_property_false(self):
        with self.assertRaises(ValueError):
            CardGame('player', TheHouse())
    def test_card_game_property1_false(self):
        with self.assertRaises(ValueError):
            CardGame(Player(), 'thehouse')
    def test_card_game_property2_false(self):
        with self.assertRaises(ValueError):
            CardGame(Player(), TheHouse(), 'asd')
    def test_card_game_property3_false(self):
        with self.assertRaises(ValueError):
            CardGame(Player(), TheHouse(), 60, 'asdsad')
            
if __name__ == '__main__':
    main()