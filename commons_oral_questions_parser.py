import json
import requests

# TODO: change for >500 results
SEARCH_ENDPOINT_URL = "http://lda.data.parliament.uk/commonsoralquestions.json?_view=Commons+Oral+Questions&_pageSize=500&_search={}&_page=0"

links_to_articles = {}


def search_articles(word, URL):
    """
    Returns a list of articles for the given word.
    """
    full_query = URL.format(word)
    response = requests.get(full_query)

    if response.status_code == 200:
        response_json = json.loads(response.text)

        for question in response_json['result']['items']:
            URL = question["_about"]

            if links_to_articles.get(word):
                links_to_articles[word].append(URL)
            else:
                links_to_articles[word] = [URL]


def search_all():
    with open("words.txt", "r") as infile:
        for line in infile:
            word = line.strip()
            search_articles(word, SEARCH_ENDPOINT_URL)

search_all()
print(links_to_articles)
