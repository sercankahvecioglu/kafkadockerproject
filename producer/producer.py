from bs4 import BeautifulSoup
import requests
import json
import time
from kafka import KafkaProducer
import os

kafka_topic = ("scrape")
kafka_server = os.getenv('KAFKA_SERVER', 'kafka:9093')

producer = KafkaProducer(
    bootstrap_servers=[kafka_server],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

link = "https://scrapeme.live/shop/"
page_to_scrape = requests.get(link)
soup = BeautifulSoup(page_to_scrape.content, "html.parser")

# Get the product links and names
products = soup.findAll("li", class_="product")

data_list = []

for product in products:
    name = product.find("h2", class_="woocommerce-loop-product__title").text
    product_link = product.find("a")["href"]

    product_page = requests.get(product_link)
    product_soup = BeautifulSoup(product_page.content, "html.parser")

    # Get the product details
    price = product_soup.find("span", "p", class_="price").text
    description = product_soup.find("div", class_="woocommerce-product-details__short-description").text.strip()
    stock = product_soup.find("p", class_="stock in-stock").text

    data_list.append({
        "name": name,
        "price": price,
        "description": description,
        "stock": stock
    })

try:
    for data in data_list:
        producer.send(kafka_topic, value = data)
        print(f'Sent: {data}')
        time.sleep(1)
except Exception as e:
    print(f"Unexpected event occured: {e}")
finally:
    producer.close()

with open('outputfile.json', 'w') as f:
    json.dump(data_list, f)
