from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#Flask setup
app = Flask(__name__)

# Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


#Flask routes:

#Rendering HTML route

@app.route("/home")
def home():


    mars_data = mongo.db.collection.find_one()


    return render_template("index.html", mars=mars_data)

#Strating the scrape route:

@app.route("/scrape")
def scrape():

    # start the scrape 
    mars_data = scrape_mars.scrape()


    mongo.db.collection.update({}, mars_data, upsert=True)

    # return to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
