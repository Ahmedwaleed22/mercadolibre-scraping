import requests
from bs4 import BeautifulSoup
import os
import csv

class FetchProducts:
  def __init__(self) -> None:
    self.BASE_DIRECTORY = './data/'
    self.DATA_CSV_FILE = os.path.join(self.BASE_DIRECTORY, 'data.csv')
    self.CSV_COLUMNS=['image', 'rating', 'name', 'price', 'old_price', 'link', 'category', 'quantity']

  def check_file_stracture(self) -> None:
    if not os.path.exists(self.BASE_DIRECTORY):
      os.mkdir(self.BASE_DIRECTORY)

    if not os.path.exists(self.DATA_CSV_FILE):
      with open(self.DATA_CSV_FILE, 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(self.CSV_COLUMNS)

  def fetch_products(self) -> None:
    request = requests.get('https://www.mercadolibre.cl/categorias')
    soup = BeautifulSoup(request.text, 'html.parser')
    all_categories_container = soup.find_all('div', class_='categories__container')

    for category_container in all_categories_container:
      title = category_container.find('a', class_='categories__title')
      sub_categories = category_container.find_all('a', class_='categories__subtitle')

      for sub_category in sub_categories:
        sub_category_name = sub_category.find('h3', class_='categories__subtitle-title')

        request = requests.get(sub_category.get('href'))
        soup = BeautifulSoup(request.text, 'html.parser')

        grid_container = soup.find('div', class_='ui-search-layout--grid__grid')

        if grid_container:
          products = grid_container.find_all('div', class_='ui-recommendations-card')
        else:
          products = []

        products_prepared_for_append = []

        for product in products:
          product_image = product.find('img', class_='ui-recommendations-card__image').get('data-src')
          product_content = product.find('div', class_='ui-recommendations-card__content')
          product_rating = product.find('span', class_='ui-recommendations-card__pill').text

          product_anchor = product_content.find('a', class_='ui-recommendations-card__link')
          product_link = product_anchor.get('href')
          product_name = product_anchor.text

          product_currency = product.find('span', class_='andes-money-amount__currency-symbol').text
          product_old_price = product_currency + product.find('span', class_='andes-money-amount__fraction').text.replace('.', ',')
          product_price = product.find('span', class_="andes-money-amount").text.replace('.', ',')

          request = requests.get(product_link)
          soup = BeautifulSoup(request.text, 'html.parser')
          quantity = soup.find('span', class_='ui-pdp-buybox__quantity__available').text
          delimiters = ["(", ")"]

          for delimiter in delimiters:
            quantity = " ".join(quantity.split(delimiter))

          products_prepared_for_append.append([
            product_image,
            product_rating,
            product_name,
            product_price,
            product_old_price,
            product_link,
            f'{title.text} > {sub_category_name.text}',
            quantity
          ])
          
        with open(self.DATA_CSV_FILE, 'a', encoding='utf-8') as csvfile:
          csvwriter = csv.writer(csvfile)
          csvwriter.writerows(products_prepared_for_append)