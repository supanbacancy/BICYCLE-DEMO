import folium
import requests

api_url = "http://127.0.0.1:5000/closest_bicycle?latitude=0.5&longitude=79&num_results=4"

response = requests.get(api_url)
data = response.json()

map_center = [data[0]['latitude'], data[0]['longitude']]
mymap = folium.Map(location=map_center, zoom_start=12)

for bike in data:
    folium.Marker(location=[bike['latitude'], bike['longitude']], popup=f"Bicycle ID: {bike['bicycle_id']}").add_to(mymap)
    
mymap.save("bicycle_map.html")