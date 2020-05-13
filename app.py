

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars

app= Flask(__name__)

#set up a mongo connection with flask_pymongo
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.replace_one({},mars_data, upsert = True)

if __name__ == "__main__":
    app.run() (debug=True)
