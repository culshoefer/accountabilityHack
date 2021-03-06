import json
import requests

# TODO: change for >500 results
SEARCH_ENDPOINT_URL = "http://lda.data.parliament.uk/commonsoralquestions.json?_view=Commons+Oral+Questions&_pageSize=50&_search={}&_page=0"
SYNONYM_ENDPOINT_URL = "http://lda.data.parliament.uk/terms.json?_view=Thesaurus&_pageSize=50&_search=%22{}%22&_page=0&_properties=prefLabel,exactMatch.prefLabel"


def get_synonyms(word):
    synonyms = [word]

    full_query = SYNONYM_ENDPOINT_URL.format(word)
    response = requests.get(full_query)

    if response.status_code == 200:
        response_json = json.loads(response.text)

        most_exact = response_json['result']['items']
        for item in most_exact:
            # fixes different structure of UK Thesauri JSON
            # sometimes exactMatch = list of strings & dictionaries
            if isinstance(item.get('exactMatch'), list):
                for sub_match in item['exactMatch']:
                    if isinstance(sub_match, dict):
                        synonyms.append(sub_match['prefLabel']['_value'])

            # sometimes exactMatch = string
            if isinstance(item.get('exactMatch'), str):
                synonyms.append(item['prefLabel']['_value'])

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

    def __repr__(self):
        return str(self)


class Topic:

    """
    Holds the topic as string and an array of all MPs talking about this topic
    String name
    Int mentions
    MP mps
    """

    def __init__(self, string, mentions):
        self.name = string
        self.mentions = mentions
        self.mps = []

    def setMentions(self, mentions):
        self.mentions = mentions

    def addMP(self, name):
        self.mps.append(MP(name))

    def incrMentions(self, value):
        self.mentions += value

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


def jdefault(o):
    return o.__dict__


def createJSON(out):
    """
    takes Output out and returns a JSON file 
    """
    with open('data.json', 'w') as outfile:
        json.dump(out, outfile, default=jdefault, indent="\t")


def printChildren(path, child, parent, numOfChildren="null"):
    s = "[" + "{\"v\": " + "\"" + str(path) + "\", " + "\"f\": " + "\"" + str(
        child) + "\"}, " + "\"" + str(parent) + "\"," + str(numOfChildren) + "],\n"

    return s


def writeTREE(output):
    f = open("o.txt", "w+")
    f.write("[\"tree\", null, 0],\n")

    tree_path = "tree"
    for topic in output.topics:
        topic_path = tree_path + "/" + topic.name
        f.write(printChildren(topic_path, topic.name, tree_path))
        for mp in topic.mps:
            mp_path = topic_path + "/" + mp.name
            try:
                f.write(printChildren(mp_path, mp.name, topic_path))
            except Exception:
                continue

            if mp.mentions.get(topic.name):
                for mention in mp.mentions.get(topic.name):
                    mention_path = mp_path + "/" + mention
                    try:
                        f.write(
                            printChildren(mention_path, mention, mp_path, "1"))
                    except Exception:
                        pass
    f.close()


finalDATA = Output()


def search_questions(word):
    """
    Returns a list of articles for the given word.
    """

    search_corpus = get_synonyms(word)[:10]

    for item in search_corpus:
        print("{} - processing {}/{}".format(word,
                                             search_corpus.index(item) + 1, len(search_corpus)))
        full_query = SEARCH_ENDPOINT_URL.format(item)
        response = requests.get(full_query)

        if response.status_code == 200:
            response_json = json.loads(response.text)
            mentions = response_json["result"]["totalResults"]

            # we are looking for the original word
            if item == word:
                finalDATA.addTopic(Topic(word, mentions))
            # count synonyms under mentions of the original
            else:
                finalDATA.topics[-1].incrMentions(mentions)

            for question in response_json['result']['items']:
                text = question['questionText']
                dt = question['modified']['_value']
                author = question['tablingMemberPrinted'][0]['_value']

                finalDATA.topics[-1].addMP(author)
                finalDATA.topics[-1].mps[-1].addMention(item, dt, text)


def search_all():
    with open("words.txt", "r") as infile:
        for line in infile:
            word = line.strip()

            print("Searching for:", word)
            search_questions(word)

###################################################
#                                                 #
#           Test Vars for json Output             #
#                                                 #
###################################################

mp1 = MP("David Cameron")
mp1.addParty("Con")
mp1.addMention("ISIS", "2015-09-29", "Who cares?")

topic_isis = Topic("ISIS", 1)
topic_isis.addMP(mp1)

output = Output()
output.addTopic(topic_isis)

createJSON(output)

###################################################
#                                                 #
#                 END OF TEST VARS                #
#                                                 #
###################################################

search_all()
createJSON(finalDATA)
writeTREE(finalDATA)
# print(finalDATA)
