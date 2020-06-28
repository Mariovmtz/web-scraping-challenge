from flask import Flask, redirect, render_template
from scrape_mars import scrape
from flask_pymongo import PyMongo
#----------------------------------------------------------
# FLASK CODE
#----------------------------------------------------------
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mission_mars'
mongo = PyMongo(app)

@app.route("/")
def main():
    latest_data=mongo.db.entries_mars.find().sort([('_id',-1)]).limit(1)
    for data in latest_data:
        return render_template("index.html", mars_data=data)


@app.route("/scrape")
def getScrape():     
    print("Scraping data from the web, please be patient")
    mars_dic = scrape()
    mongo.db.entries_mars.insert(mars_dic)
    return redirect("/")



if __name__ == '__main__':
    app.run(debug=True)
