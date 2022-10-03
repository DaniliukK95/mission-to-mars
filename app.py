# import our tools #10.5.1
# flask to render a template, redirecting to another URL, and creating a URL
from flask import Flask, render_template, redirect, url_for
# use PyMongo to interact with Mongo database
from flask_pymongo import PyMongo
#use the scraping code, convert from JNB to Python. 
import scraping


# set up flask 
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# define route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)


#set up the scraping route (the Button)
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

# last code needed to tell flask to run. 
if __name__ == "__main__":
   app.run()
