import pymongo

import scrape_mars

# 1. import Flask
from flask import Flask, render_template

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.scrape



# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    items = db.items.find()

    for item in items:
        print(item)
        print(type(item))
        return render_template("index.html", dict=item)

# 4. Define what to do when a user hits the /about route
@app.route("/scrape")
def scrape():
    print("Scraping...")

    data = scrape_mars.scrape()
    collection = db.items
    collection.insert_one(data)
    return "success"


if __name__ == "__main__":
    app.run(debug=True)

#Need to put this into MongoDB