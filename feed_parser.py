import requests as r
import xml.etree.ElementTree as ET

FEED_URL = "http://api.data.parliament.uk/resources/files/feed?dataset=12"
xml_response = r.get(FEED_URL)

if xml_response.status_code == 200:
    root = ET.fromstring(xml_response.text)
    print(root)

    for child in root:
        for elem in child:
            entry = elem.attrib

            if entry.get('href') is not None:
                print(entry['href'])
