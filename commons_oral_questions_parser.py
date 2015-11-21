import json
import requests

# TODO: change for >500 results
SEARCH_ENDPOINT_URL = "http://lda.data.parliament.uk/commonsoralquestions.json?_view=Commons+Oral+Questions&_pageSize=500&_search={}&_page=0"
SYNONYM_ENDPOINT_URL = "http://lda.data.parliament.uk/terms.json?_view=Thesaurus&_pageSize=500&_search=%22{}%22&_page=0&_properties=prefLabel,exactMatch.prefLabel"


def get_synonyms(word):
    synonyms = []

    full_query = SYNONYM_ENDPOINT_URL.format(word)
    response = requests.get(full_query)

    if response.status_code == 200:
        response_json = json.loads(response.text)

        most_exact = response_json['result']['items'][0]
        for match in most_exact['exactMatch']:
            # if the match is not an URL
            if isinstance(match, dict):
                synonyms.append(match['prefLabel']['_value'])

    return synonyms

class Output:
    def __init__(self):
        self.topics = []

    def addTopic(self, topic):
        self.topics.append(topic)

    def sort(self):
        """
        sorts the Topic topics[]
        Topic being mentioned most is at topics[0]
        """
        pass

    def __str__(self):
        result = ""
        for topic in self.topics:
            result = result + str(topic) + "\n"
        return result


class Topic:

    """
    String name
    Int mentions
    MP mps
    """

    def __init__(self, string, mentions):
        self.name = string
        self.mentions = mentions
        self.mps = []

    def addMP(self, name):
        self.mps.append(MP(name))

    def __str__(self):
        return "{}: {}".format(self.name, self.mentions)

    def __repr__(self):
        return str(self)


class MP:

    """
    Class holding all mentions the MP did to a specific topic as dict
    Dict mentions = {'String topic' : ["String", "String" , "String"]}
    String name
    String party
    """

    def __init__(self, name):
        self.name = name
        self.mentions = {}

    def addParty(self, party):
        self.party = party

    def addMention(self, topic, date, text):
        s = date + "#" + text
        if topic in self.mentions.keys():
            self.mentions[topic].append(s)
        else:
            self.mentions[topic] = [s]

    def __str__(self):
        return "{} {}".format(self.name, self.mentions)

    def __repr__(self):
        return str(self)

finalDATA = Output()


def search_questions(word):
    """
    Returns a list of articles for the given word.
    """

    full_query = SEARCH_ENDPOINT_URL.format(word)
    response = requests.get(full_query)

    if response.status_code == 200:
        response_json = json.loads(response.text)
        mentions = response_json["result"]["totalResults"]

        finalDATA.addTopic(Topic(word, mentions))

        for question in response_json['result']['items']:
            text = question['questionText']
            dt = question['modified']['_value']
            author = question['tablingMemberPrinted'][0]['_value']

            finalDATA.topics[-1].addMP(author)
            finalDATA.topics[-1].mps[-1].addMention(word, dt, text)


def search_all():
    with open("words.txt", "r") as infile:
        for line in infile:
            word = line.strip()

            search_questions(word)
search_all()

for topic in finalDATA.topics:
    print(topic)