from re import T
import pandas as pd
import os
from Scarper import BCCScraper
from URL import URL
from Exceptions import *

def create_url_object(url):
  try:
    url_object = URL(url)
    return url_object
  except InvaildURL:
    return None

def get_url_inputs():
  con = "y"
  urlArr = []
  while len(con) > 0 and con[0] == "y":
    url = input("Enter url: ")
    url_object = create_url_object(url)

    if url_object:
      urlArr.append(url_object)
      
    con = input("Enter yes to enter another url: ")
  return urlArr


if __name__ == "__main__":
  url_inputs = get_url_inputs()
  df = BCCScraper.create_excel_urlArray(url_inputs)