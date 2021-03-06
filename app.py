from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")
first=True

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # print(mongo)
    # Find one record of data from the mongo database
    data = mongo.db.collection.find_one()
    for i in mongo.db.collection.find():
        print(i.get("_id"))

    # print(data)
    # Return template and data
    return render_template("index.html", data=data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # first = False
    # Run the scrape function
    data = scrape_mars.scrape()
    
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.find_one_and_replace({},data,upsert=True)


    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
