import requests as r
import xml.etree.ElementTree as ET

FEED_URL_DAILY = "http://api.data.parliament.uk/resources/files/feed?dataset=12"
FEED_URL_MOHTLY = "http://api.data.parliament.uk/resources/files/feed?dataset=14"

xml_response = r.get(FEED_URL_DAILY)

if xml_response.status_code == 200:
    root = ET.fromstring(xml_response.text)

    for child in root:
        for elem in child:
            entry = elem.attrib

            if entry.get('href') is not None:
                print(entry['href'])
