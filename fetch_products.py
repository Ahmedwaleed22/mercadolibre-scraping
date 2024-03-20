from operations.fetch import FetchProducts

def main():
  fetch_products = FetchProducts()
  fetch_products.check_file_stracture()
  fetch_products.fetch_products()

if __name__ == '__main__':
  main()