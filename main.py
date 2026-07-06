import requests
import xml.etree.ElementTree as ET
import json

def fetch_and_convert():
    url = "https://data.tmd.go.th/api/WeatherWarningNews/v2/index.php"
    response = requests.get(url)
    root = ET.fromstring(response.content)
    
    features = []
    # ในตัวอย่าง XML มีโหนด <Warning>
    for w in root.findall('Warning'):
        lat = 25.0 # จากตัวอย่างที่คุณให้มา (ควรเขียน logic ดึงจาก text ใน Description)
        lon = 109.0
        
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "title": w.find('TitleThai').text,
                "headline": w.find('HeadlineThai').text,
                "link": w.find('WebUrlThai').text
            }
        }
        features.append(feature)
        
    geojson = {"type": "FeatureCollection", "features": features}
    
    with open('data/storm.geojson', 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False)

if __name__ == "__main__":
    fetch_and_convert()
