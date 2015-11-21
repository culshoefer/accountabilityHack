import requests as r
import xml.etree.ElementTree as ET

FEED_URL = "http://api.data.parliament.uk/resources/files/feed?dataset=12"
xml_response = r.get(FEED_URL)

if r.status_code == 200:
    tree = ET.parse(xml_response)
    root = tree.getroot()

    print(root)
