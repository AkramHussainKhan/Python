#importing librries
import time

import pandas as pd
import requests


class Pharma:
  def __init__(self):
    self.data = []
    self.parse()
    
  def parse(self):
    for page in range(1,6):
      url = f'https://pharmeasy.in/api/otc/getCategoryProducts?categoryId=9190&page={page}'
      req = requests.get(url)
      time.sleep(1)
      print(10*'#')
      print(str(page) +" "+ 'done')
      response = req.json()
      for product in range(20):
        try:
          name = response['data']['products'][product]['name']
          manu = response['data']['products'][product]['manufacturer']
          mpde = response['data']['products'][product]['mrpDecimal']
          sde = response['data']['products'][product]['salePriceDecimal']
          vote_rate = response['data']['products'][product]['ratingDetails']['count']
          rating = round(response['data']['products'][product]['ratingDetails']['value'],2)
          discount_d = response['data']['products'][product]['discountDecimal']
          discount_p = response['data']['products'][product]['discountPercent']
          p_vol = response['data']['products'][product]['productVolume']
        except:
          name = "None"
          manu = "None"
          mpde = "None"
          sde = "None"
          vote_rate = "None"
          rating = "None"
          discount_d = "None"
          discount_p = "None"
          p_vol = "None"
        data_json = {
            'product_name' : name,
            'manufacturer' : manu,
            'mrpDecimal': mpde,
            'salePriceDecimal': sde,
            'discountDecimal': discount_d,
            'discountPercent': discount_p,
            'vote_for_rating': vote_rate,
            'rating': rating,
            'productVolume': p_vol
          }
        self.data.append(data_json)
        self.export()
  def export(self):
     df = pd.DataFrame(self.data)
     df.to_csv('pharma_data.csv', index=False)

if __name__ == '__main__':
    scrape = Pharma()
    scrape.parse()
