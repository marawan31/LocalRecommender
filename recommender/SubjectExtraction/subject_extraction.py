# python3 -m pip install spacy nltk
# python3 -m spacy download en_core_web_sm
from nltk.corpus import stopwords
import spacy

def get_hashtags(sentence):
    hashtags = list(filter(lambda x:x[0] == '#', sentence.split()))
    return [h[1:] for h in hashtags], " ".join(filter(lambda x:x[0] != '#', sentence.split())) 

def remove_links(sentence):

    return " ".join(filter(lambda x:x[0:4] != 'http', sentence.split())) 

def get_topic(sentence):
    parser = spacy.load("en_core_web_sm")
    stop_words = set(stopwords.words('english')) 

    sentence_wo_links = remove_links(sentence)
    hashtags, sentence_wo_hashtags = get_hashtags(sentence_wo_links)
    doc = parser(sentence_wo_hashtags)

    subjects = [entity.text for entity in doc.ents] + hashtags

    # Remove stop words in each sentence
    new_subjects = []
    for sentence in subjects:
        new_sentence = ""
        for word in sentence.split(" "):
            if not word in stop_words:
                new_sentence += word + " "
        new_subjects.append(new_sentence.strip())

    # Remove duplicates
    filtered_subjects = list(set(new_subjects))
    return filtered_subjects
