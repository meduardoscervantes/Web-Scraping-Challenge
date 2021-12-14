from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape_all

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():
    listings = mongo.db.listings.find_one()
    return render_template("index.html", listings=listings)


@app.route("/scrape")
def scraper():
    listings = mongo.db.listings
    listings.drop()
    listings_data = scrape_all()
    listings.insert_one(listings_data)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
