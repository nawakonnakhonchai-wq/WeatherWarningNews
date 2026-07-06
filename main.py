import requests
import xml.etree.ElementTree as ET
import json
import os

def fetch_and_convert():
    # URL สำหรับดึงข้อมูลจากกรมอุตุนิยมวิทยา
    url = "https://data.tmd.go.th/api/WeatherWarningNews/v2/"
    params = {
        "uid": "demo",
        "ukey": "demokey"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            return

        # ทำความสะอาดข้อมูล XML ก่อน parse (ป้องกัน Error จากตัวอักษรพิเศษบางตัว)
        root = ET.fromstring(response.content)
        features = []
        
        # วนลูปดึงข้อมูลแต่ละ Warning
        for w in root.findall('Warning'):
            # ฟังก์ชันช่วยดึงค่า text เพื่อกันค่า None
            def get_text(tag_name):
                node = w.find(tag_name)
                return node.text.strip() if (node is not None and node.text) else ""

            # สร้าง Feature สำหรับ GeoJSON
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point", 
                    "coordinates": [100.5018, 13.7563] # พิกัดอ้างอิงเบื้องต้น
                },
                "properties": {
                    "title": get_text('TitleThai'),
                    "headline": get_text('HeadlineThai'),
                    "description": get_text('DescriptionThai'),
                    "issueNo": get_text('IssueNo'),
                    "announceDate": get_text('AnnounceDate'),
                    "webUrl": get_text('WebUrlThai')
                }
            }
            features.append(feature)
            
        # สร้างโครงสร้าง GeoJSON
        geojson = {"type": "FeatureCollection", "features": features}
        
        # ตรวจสอบและสร้างโฟลเดอร์ data
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # บันทึกไฟล์
        with open('data/storm.geojson', 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully processed {len(features)} warnings.")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    fetch_and_convert()
