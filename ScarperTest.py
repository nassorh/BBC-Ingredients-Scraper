import unittest

from pytest import importorskip
from URL import URL
from Scarper import BCCScraper
from Exceptions import *
import numpy as np
from main import create_url_object
import filecmp

class ScraperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.url = URL("https://www.bbc.co.uk/food/recipes/avocado_pasta_with_peas_31700")
        cls.scarper = BCCScraper(cls.url)

    def test_update_soup(self):
        print("Test Update Soup")
        self.assertEqual(0,self.scarper.update_soup())

    def test_update_jsonRecipes(self):
        print("Test Update jsonRecipe")
        self.assertEqual(0,self.scarper.update_jsonRecipes())

    def test_get_cookTime(self):
        print("Test get cookTime")
        self.assertEqual(10,self.scarper.get_cookTime())

    def test_get_prepTime(self):
        print("Test get prepTime")
        self.assertEqual(30,self.scarper.get_prepTime())
    
    def test_get_totalTime(self):
        print("Test get totalTime")
        self.assertEqual(40,self.scarper.get_totalTime())

    def test_get_title(self):
        reactInitialState = self.scarper.fetch_reactInitialState_JSON()
        print("Test get title")
        self.assertEqual("Avocado pasta with peas and mint ",self.scarper.get_title(reactInitialState))

    def test_get_image(self):
        print("Test get image")
        self.assertEqual("https://food-images.files.bbci.co.uk/food/recipes/avocado_pasta_with_peas_31700_16x9.jpg",self.scarper.get_image())

    def test_get_ingredients(self):
        print("Test get ingredients")
        reactInitialState = self.scarper.fetch_reactInitialState_JSON()
        
        ingredients = "375g/13oz pasta, such as penne or fusilli, 1 large avocado (or 2 small) , 2 garlic cloves, 2 tbsp coconut oil, melted, ½ tsp salt , 1 lemon, juice and zest , 6 fresh mint leaves, 150g/5½oz fresh peas (or frozen and defrosted) , 1 large red chilli (optional) "
        self.assertEqual(ingredients,self.scarper.get_ingredients(reactInitialState))

    def test_get_rating_val(self):
        print("Test get rating value")
        self.assertEqual(4,self.scarper.get_rating_val())

    def test_get_rating_count(self):
        print("Test get rating count")
        self.assertEqual(24,self.scarper.get_rating_count())

    def test_get_category(self):
        print("Test get category")
        self.assertEqual("Main course",self.scarper.get_category())

    def test_get_cuisine(self):
        print("Test get cuisine")
        reactInitialState = self.scarper.fetch_reactInitialState_JSON()
        
        self.assertTrue(np.isnan(self.scarper.get_cuisine(reactInitialState)))

    def test_get_diet(self):
        print("Test get diet")
        reactInitialState = self.scarper.fetch_reactInitialState_JSON()
        
        self.assertEqual("dairy-free, egg-free, healthy, nut-free, pregnancy-friendly, vegan, vegetarian",self.scarper.get_diet(reactInitialState))

    def test_scraper(self):
        print("Scraper Test")
        urlArr = ["https://www.bbc.co.uk/food/recipes/avocado_pasta_with_peas_31700","https://www.bbc.co.uk/food/recipes/paneerwithspinach_86756","https://www.bbc.co.uk/food/recipes/crab_linguine_22025","https://www.bbc.co.uk/food/recipes/upside-down_pineapple_63080","https://www.bbc.co.uk/food/recipes/roasted_figs_wrapped_in_44423","https://www.bbc.co.uk/food/recipes/aged_sirloin_steak_with_62354"]
        
        url_obj_array = []
        for url in urlArr:
            url_obj = create_url_object(url)
            url_obj_array.append(url_obj)

        BCCScraper.create_excel_urlArray(url_obj_array)
        self.assertTrue(filecmp.cmp('Test Example.csv', 'BBC Recipe Data.csv'))

if __name__ == "__main__":
    unittest.main()
