from flask import Flask, request, jsonify
from rtree import index
import mysql.connector

app = Flask(__name__)

idx = index.Index()

# Connect to MySQL
connection = mysql.connector.connect(
    host="mysql",
    user="root",
    password="my-secret-pw",
    database="bicycle_data"
)
cursor = connection.cursor()
cursor.execute("SELECT latitude, longitude, bicycle_id FROM bicycle_location")
bicycle_data = cursor.fetchall()

for i, (latitude, longitude, _) in enumerate(bicycle_data):
    idx.insert(i, (latitude, longitude))

@app.route('/closest_bicycle', methods=['GET'])
def closest_bicycle():
    try:
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        num_results = int(request.args.get('num_results', 1))
    except ValueError:
        return jsonify({'error': 'Invalid latitude, longitude, or num_results provided'}), 400

    closest_idxs = list(idx.nearest((latitude, longitude), num_results))
    closest_bicycles = [bicycle_data[idx] for idx in closest_idxs]

    response = []
    for bicycle in closest_bicycles:
        response.append({
            'bicycle_id': bicycle[2],
            'latitude': bicycle[0],
            'longitude': bicycle[1]
        })

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
