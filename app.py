from flask import Flask, request,render_template, jsonify
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

db = client["test"]
collection = db["flask-tutorial"]

try:
    client.admin.command("ping")
    print("Connected successfully!")
except Exception as e:
    print(e)

client = MongoClient(
    MONGO_URI,
    server_api=ServerApi('1'),
    serverSelectionTimeoutMS=5000
)

app = Flask(__name__)

@app.route('/')
def home():
    day_of_week = datetime.now().strftime("%A") 
    current_time = datetime.now().strftime("%H:%M:%S")


    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)
@app.route('/submit', methods=['POST'])
def submit():
   form_data = dict(request.form)
    
   collection.insert_one(form_data)

   return 'data submited successfully!'
@app.route('/view')
def view():
    data = collection.find()
    data = list(data)

    for item in data:
        print(item)

        del item['_id']

    data = {
        'data': data
    }
    return data


@app.route('/get-data')
def get_data():
    data = list(collection.find({}, {"_id": 0}))

    return jsonify({
        "status": "success",
        "count": len(data),
        "data": data
    })

if __name__ == "__main__":
    app.run(debug=True)
