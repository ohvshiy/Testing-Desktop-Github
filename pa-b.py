import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from time import sleep
from PIL import Image
from pytesseract import image_to_string


def get_html(url):
	r = requests.get(url)
	return r.text

def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')

	pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
	total_pages = pages.split('=')[1].split('&')[0]

	return int(total_pages)

def write_csv(data):
	with open('avito.csv', 'a', errors='ignore') as f:
		writer = csv.writer(f, delimiter=';')
		
		
		writer.writerow( (data['title'], 
			              data['price'], 
			              data['published'], 
			              data['url'],
			              data['str_phone']) )




def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')

	ads = soup.find('div', class_='js-catalog_serp').find_all('div', class_='item_table')
	for ad in ads:

		name = ad.find('div', class_='description').find('h3').text.strip().lower()

		if 'бытовка' in name:


			try:
				title = ad.find('div', class_='description').find('h3').text.strip()
				print(title)

			except:
				title = ''

			try:
				price = ad.find('div', class_='snippet-price-row').text.strip()
				print(price)
			
			except:
				price = ''
		

			try:
				published = ad.find('div', class_='snippet-date-info').text.strip()
				print(published)

			except:
				published = ''
				

			try:
				url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href').strip()
				
	
			except:
				url = ''

			try:
				url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href').strip()
				browser = webdriver.Firefox()
				ovn = browser.get(url)
				button = browser.find_element_by_xpath('//button[@class="button-button-2Fo5k button-size-l-3LVJf button-primary-1RhOG width-width-12-2VZLz"]')
				button.click()
				sleep(3)
				browser.save_screenshot('number_phone.png')
				image = browser.find_element_by_class_name('contacts-phone-3KtSI')
				location = image.location
				size = image.size
				crops = Image.open('number_phone.png')
				x = location['x']
				y = location['y']
				width = size['width']
				height = size['height']


				crops.crop((x, y, x + width, y + height)).save('vagon.gif')
				crops2 = Image.open('vagon.gif')
				str_phone = image_to_string(crops2)
				print(str_phone)
				browser.quit()
				
	
			except:
				str_phone = ''

			
			data = {'title': title, 
			        'price': price, 
			        'published': published,
			        'url': url,
			        'str_phone': str_phone}
			
			write_csv(data)
			
			
			
		else:
			continue	





def main():
	url = "https://www.avito.ru/irkutsk?q=%D0%B2%D0%B0%D0%B3%D0%BE%D0%BD%D1%87%D0%B8%D0%BA+%D0%B1%D1%8B%D1%82%D0%BE%D0%B2%D0%BA%D0%B0&p=1"
	base_url = 'https://www.avito.ru/irkutsk?'
	category_part = 'q=%D0%B2%D0%B0%D0%B3%D0%BE%D0%BD%D1%87%D0%B8%D0%BA+%D0%B1%D1%8B%D1%82%D0%BE%D0%B2%D0%BA%D0%B0&'
	page_part = 'p='

	total_pages = get_total_pages(get_html(url))

	for i in range(1, total_pages + 1):
		url_gen = base_url + category_part + page_part + str(i)
		print(url_gen)
		html = get_html(url_gen)
		get_page_data(html)





if __name__ == '__main__':
	main()




