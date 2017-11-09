from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta
from flask import Flask
import datetime as dt
import scrap_mars 
from scrap_mars  import scrape
from flask import render_template


app = Flask(__name__)
@app.route("/")
def welcome():
        conn = 'mongodb://admin:nagamongo@ds033106.mlab.com:33106/heroku_6z3mdtrf'
        client = pymongo.MongoClient(conn)
        db = client.heroku_6z3mdtrf
        collection = db.marsdata.find_one({})
        return render_template('index.html',marsData=collection)
@app.route("/scrape")    
def data():
    try:
        x = scrape()
        conn = 'mongodb://admin:nagamongo@ds033106.mlab.com:33106/heroku_6z3mdtrf'
        client = pymongo.MongoClient(conn)

        # Define database and collection
        db = client.heroku_6z3mdtrf
        collection = db.marsdata
        collection.replace_one({},x,upsert=True)
        return ('success')
    except Exception as e:
        return e
if __name__ == '__main__':
    app.run(debug=True)

    


