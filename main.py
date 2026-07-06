import requests
import xml.etree.ElementTree as ET
import json
import os

def fetch_and_convert():
    url = "https://data.tmd.go.th/api/WeatherWarningNews/v2/"
    params = {
        "uid": "demo",
        "ukey": "demokey"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        try:
            root = ET.fromstring(response.content)
            features = []
            
            # โครงสร้าง XML ของ TMD มักจะมีรายการ Warning อยู่ข้างใน
            for w in root.findall('Warning'):
                # ดึงข้อมูลจาก XML
                title = w.find('TitleThai').text if w.find('TitleThai') is not None else "ไม่มีหัวข้อ"
                headline = w.find('HeadlineThai').text if w.find('HeadlineThai') is not None else ""
                
                # เนื่องจากพิกัดไม่ได้เป็นตัวเลขแยกต่างหาก เราอาจต้องให้จุดศูนย์กลางไว้ที่ไทยก่อน 
                # หรือหาคำใน Description หากคุณต้องการ Plot บนแผนที่
                feature = {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [100.5018, 13.7563]}, # พิกัดกรุงเทพฯ (เบื้องต้น)
                    "properties": {
                        "title": title,
                        "headline": headline,
                        "date": w.find('AnnounceDate').text if w.find('AnnounceDate') is not None else ""
                    }
                }
                features.append(feature)
                
            geojson = {"type": "FeatureCollection", "features": features}
            
            if not os.path.exists('data'):
                os.makedirs('data')
                
            with open('data/storm.geojson', 'w', encoding='utf-8') as f:
                json.dump(geojson, f, ensure_ascii=False, indent=4)
            print("Successfully updated storm.geojson")
            
        except Exception as e:
            print(f"Error parsing XML: {e}")
    else:
        print(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    fetch_and_convert()
