from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():

    # Find the first record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars_dict=mars_dict)

@app.route("/scrape")
def scrape():

    mars_dict=mongo.db.mars_dict

    # Run the scrape function
    mars_dict_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_dict.update({}, mars_dict_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
