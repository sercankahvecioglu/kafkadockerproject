from flask import Flask, jsonify
import json

app = Flask(__name__)

# Function to read data from the JSON file
def read_data_from_file():
    with open('/data/outputfile.json', 'r') as file:
        data = json.load(file)
    return data

# Route to get all data
@app.route('/data', methods=['GET'])
def get_data():
    data = read_data_from_file()
    return jsonify(data)

@app.route('/')
def home():
    return "Sercan's API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)