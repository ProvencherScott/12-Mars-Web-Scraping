from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

#Use flask_pymongo to set up mongo conection
app.config["MONGO_URI"] = 'mongodb://localhost:27017/mars_data_app'
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    mars = mongo.db.mars.find_one()
    #print(mars_data)
    return render_template("index.html", mars=mars)

# Route to render for data scraping
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars_data
    mars_data = scrape_mars.scrape()
    # print (mars_info)
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)