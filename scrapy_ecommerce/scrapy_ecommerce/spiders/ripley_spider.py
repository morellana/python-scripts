import scrapy
import re

class RipleySpider(scrapy.Spider):
	name = "ripley"
	SMARTPHONES_URL = 'http://simple.ripley.cl/telefonia/celulares/smartphones?page='

	start_urls = [
		SMARTPHONES_URL+'1'
	]


	def parse(self, response):
		for product in response.css('div.product-description'):
			name = product.css("span.catalog-product-name::text").extract_first().strip()
			normal_price = 	product.css("span.catalog-product-list-price::text").extract_first()
			internet_price = product.css("span.catalog-product-offer-price::text").extract_first()
			card_price = product.css("span.catalog-product-card-price::text").extract_first()
			
			card_price = card_price.strip() if card_price != None else None # clean data

			yield {
				'name': name,
				'normal_price': self.getPrice(normal_price),
				'internet_price': self.getPrice(internet_price),
				'card_price': self.getPrice(card_price)
			}

			totalPages = int(re.findall(r'totalPages":(.*?),',response.body)[0])
			for i in range(2,totalPages+1):
				yield scrapy.Request(self.SMARTPHONES_URL+str(i), callback=self.parse)

			
	def getPrice(self, text):
		if text == None:
			return None
			
		price = ''
		for letter in text:
			if ord(letter) >= 48 and ord(letter) <= 57:
				price += letter
		return price
