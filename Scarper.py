from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
import re 
import json
import numpy as np
from Exceptions import *
import pandas as pd

class BCCScraper():
    def __init__(self,URL):
        self.url = URL 
        self.soup = None
        self.jsonRecipes = None
        
    def update_soup(self):
        if self.soup == None:
            #Ignore SSL certificate errors
            sll_contex = self.get_ignore_ssl_certificate_errors_context()
            document = urlopen(self.url.link, context=sll_contex)
            html = document.read()
            self.soup = BeautifulSoup(html, "html.parser")
        return 0

    def get_ignore_ssl_certificate_errors_context(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def collect_page_data(self):
        reactInitialState = self.fetch_reactInitialState_JSON()
        title = self.get_title(reactInitialState)
        totalTime = self.get_totalTime()
        image = self.get_image()
        ingredients = self.get_ingredients(reactInitialState)
        rating_val = self.get_rating_val()
        rating_count = self.get_rating_count()
        category = self.get_category()
        cuisine = self.get_cuisine(reactInitialState)
        diet = self.get_diet(reactInitialState)
        vegan = self.fetchDiet("vegan",diet)
        vegetarian = self.fetchDiet("vegetarian",diet)
        return [title,totalTime,image,ingredients,rating_val,rating_count,category,cuisine,diet,vegan,vegetarian,self.url.link]

    def get_title(self,reactInitialState):
        try:
            title = reactInitialState["recipeReducer"]["recipe"]["title"]
            return title
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan

    def get_totalTime(self):
        totalTime = self.get_cookTime() + self.get_prepTime()
        return totalTime

    def update_jsonRecipes(self):
        if self.jsonRecipes == None:
            self.update_soup()
            try:
                script = self.soup.find("script", {"type": "application/ld+json"})
                self.jsonRecipes = json.loads(script.string)
            except AttributeError:
                raise InvaildTag()
        
        return 0

    def get_cookTime(self):
        self.update_jsonRecipes()
        try:
            cookTime = int(self.jsonRecipes["cookTime"][2:4])
            return cookTime
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan

    def get_prepTime(self):
        try:
            self.update_jsonRecipes()
            prepTime = int(self.jsonRecipes["prepTime"][2:4])
            return prepTime
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan

    def get_image(self):
        try:
            self.update_jsonRecipes()
            image = self.jsonRecipes["image"][0]
            return image
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan
    
    def get_ingredients(self,reactInitialState):
        try:
            ingredients = ", ".join([ingredientText["text"] for ingredient in reactInitialState["recipeReducer"]["recipe"]["stagesWithoutLinks"] for ingredientText in ingredient["ingredients"]])
            return ingredients
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan

    def get_rating_val(self):
        try:
            self.update_jsonRecipes()
            rating_val = round(self.jsonRecipes["aggregateRating"]["ratingValue"])
            return rating_val
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan

    def get_rating_count(self):
        try:
            self.update_jsonRecipes()
            rating_count = self.jsonRecipes["aggregateRating"]["ratingCount"]
            return rating_count
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan

    def get_category(self):
        try:
            self.update_jsonRecipes()
            category = self.jsonRecipes["recipeCategory"]
            return category
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan
    
    def get_cuisine(self,reactInitialState):
        try:
            cuisine = reactInitialState["recipeReducer"]["recipe"]["cuisine"]["title"]
            return cuisine
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan
        except TypeError:
            return np.nan

    def get_diet(self,reactInitialState):
        try:
            diet = ", ".join([diet["title"] for diet in reactInitialState["recipeReducer"]["recipe"]["diets"]])
            return diet
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan

    def fetch_reactInitialState_JSON(self):
        try:
            script = self.fetch_reactInitialState()
            script = script[0].strip()
            script = script[script.index("{"):]
            script = script[0:-1] #Remove semi column at then 
            scriptJson = json.loads(script)
            return scriptJson
        except KeyError:
            return np.nan
        except TypeError:
            return np.nan
    
    def fetch_reactInitialState(self):
        reactInitialState_tag = r'window\.__reactInitialState__ = ({.*});'

        script = self.soup.findAll(text=re.compile(reactInitialState_tag))
        if len(script) == 0:
            raise InvaildTag("Could not find "+reactInitialState_tag+" in soup")
        else:
            return script

    def fetchDiet(self,dietType,diet):
        if diet == np.nan:
            return np.nan

        if dietType in diet.lower():
            return True
        else:
            return False
    


    @classmethod
    def create_excel_urlArray(cls,urls):
        numpy_array = cls.scrape_urls(urls)
        df = pd.DataFrame(numpy_array,columns=['title', 'total_time', 'image', 'ingredients', 'rating_val', 'rating_count',
        'category', 'cuisine', 'diet', 'vegan', 'vegetarian', 'url'])
        df.to_csv("BBC Recipe Data.csv",index=False)
        return df

    @classmethod
    def scrape_urls(cls,urlArray):      
        scrape_array = []

        for url in urlArray:
            scraper = cls.create_scraper(url)
            
            if scraper:
                numpy_array = np.array(scraper.collect_page_data())
                scrape_array.append(numpy_array)
            else:
                print("Invalid URL:",scraper.url,"-Failed to create soup")

        return np.array(scrape_array)

    @staticmethod
    def create_scraper(url):
        scraper = BCCScraper(url)
        scraper.update_soup()

        if scraper.soup:
            return scraper
        else:
            return None

    
