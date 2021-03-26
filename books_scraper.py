import sqlite3
import requests
from bs4 import BeautifulSoup

def scraper_books(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	books = soup.find_all("article")

	all_books = []
	for book in books:
		book_data = (get_title(book), get_price(book), get_rating(book))
		all_books.append(book_data)
	save_books(all_books)

def save_books(all_books):
	conn = sqlite3.connect("books.db")
	c = conn.cursor()

	c.execute('''CREATE TABLE books
		(title TEXT, price REAL, rating INTEGER)''')
	c.executemany("INSERT INTO books VALUES (?,?,?)", all_books)

	conn.commit()
	conn.close()

def get_title(book):
	return book.find("h3").find("a")["title"]

def get_price(book):
	price = book.find(class_="price_color").get_text()
	return float(price.replace("Â£", ""))

def get_rating(book):
	paragraph = book.find(class_="star-rating")
	ratings = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
	word = paragraph.get_attribute_list("class")[-1]
	return ratings[word]

scraper_books("http://books.toscrape.com/catalogue/category/books/history_32/index.html")