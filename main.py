import requests
from bs4 import BeautifulSoup
import mysql.connector
import re
from sklearn import tree
cnx = mysql.connector.connect(user='root',
                              password='09109534220',
                              database='truecar')
cursor = cnx.cursor()
first_query = 'CREATE TABLE cars (price VARCHAR(20), miles VARCHAR(20), Year VARCHAR(20))'
cursor.execute(first_query)
cnx.commit()

car_name = input('enter car name :')
car_name = re.sub(r' ', '/', car_name)
car_name = re.sub(r'-', '/', car_name)


for number in range(1, 11):
    req = requests.get(f'https://www.truecar.com/used-cars-for-sale/listings/{car_name}/?page={number}')
    soap = BeautifulSoup(req.text, 'html.parser')

    prices = soap.find_all(attrs={'data-test': ["vehicleListingPriceAmount"]})
    mileage = soap.find_all(attrs={'data-test': ["vehicleMileage"]})
    years = soap.find_all(attrs={'class': ["vehicle-card-year text-xs"]})

    for i in range(len(prices)):
        help_price = re.sub(r'(\$.+)(\$.)+', r'\2', prices[i].text)
        help_price = re.sub(r',', '', help_price)
        help_price = re.sub(r'\$', '', help_price)
        help_miles = re.sub(r'miles', '', mileage[i].text)
        help_miles = re.sub(r',', '', help_miles)
        second_query = 'INSERT INTO cars VALUES(\'{}\', \'{}\', \'{}\')'.format(int(help_price), int(help_miles),
                                                                                int(years[i].text))
        cursor.execute(second_query)

cnx.commit()
third_query = 'SELECT * FROM cars'
cursor.execute(third_query)
x = list()
y = list()
for p, m, ye in cursor:
    x.append([m, ye])
    y.append(p)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

new_data = [[1000, 2023], [55000, 2017], [90000, 2016]]
answer = clf.predict(new_data)  # bmw x4 price 50k-60k, 25k-35k, 15k-25k
for i in range(len(new_data)):
    print(answer[i])
cnx.commit()
cnx.close()
