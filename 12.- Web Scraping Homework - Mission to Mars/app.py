from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Setup Pymongo
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars

# Flask App
app = Flask(__name__)

@app.route('/')
def home():
	mars = collection.find_one()
	return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
	scrape_mars.scrape()
	

 


if __name__ == "__main__":
    app.run(debug=True)
