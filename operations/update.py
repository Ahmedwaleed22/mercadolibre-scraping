import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

class UpdateInventory:
  def __init__(self) -> None:
    self.BASE_DIRECTORY = './data/'
    self.DATA_CSV_FILE = os.path.join(self.BASE_DIRECTORY, 'data.csv')

  def update(self) -> None:
    df = pd.read_csv(self.DATA_CSV_FILE)

    for index, row in df.iterrows():
      product_name = row['name']
      product_link = row['link']

      request = requests.get(product_link)
      soup = BeautifulSoup(request.text, 'html.parser')
      quantity = soup.find('span', class_='ui-pdp-buybox__quantity__available').text
      delimiters = ["(", ")"]

      for delimiter in delimiters:
        quantity = " ".join(quantity.split(delimiter))

      row['quantity'] = quantity

    df.to_csv(self.DATA_CSV_FILE, index=False)