
try:
    import wikipedia
except:
    print("Wikipedia package not installed, but can use already downloaded data.")
from json import dump, load
import nltk
import numpy
from scipy import spatial
from math import log

# Heavily inspired by the answers given for Lab 2

class PlaceSimilarity:
    def __init__(self):
        self.cities = [
            "Paris",
            "London",
            "Berlin",
            "Rome",
            "Madrid",
            "Barcelona",
            "Vienna",
            "Amsterdam",
            "Brussels",
            "Budapest",
            "Bangkok",
            "Tokyo",
            "Beijing",
            "Los Angeles",
            "Chicago",
            "Dubai",
            "Singapore",
            "Rhodes",
            "Miami"
        ]
        self.bow, self.vocab = self.load_maxtrix_and_bow_and_vocab()


    def tfidf_weighting(self, bow):
        # N = number of documents
        # n = number of documents containing that term
        # d = document
        # t = term
        tfidf_vectors = {}
        N = len(bow)
        for city, vector in bow.items():
            print(f"Calculating tfidf for {city}")
            tfidf_vector = []
            for index, frequency in enumerate(vector):
                tf = log(1 + frequency)
                n = sum([1 for v in bow.values() if frequency in v])
                idf = log(N / n)
                tfidf_vector.append(tf*idf)
            tfidf_vectors[city] = tfidf_vector
        return tfidf_vectors


    def createVector(self, vocab, tokens):
        # regular frequency weighting
        vector = numpy.zeros(len(vocab))
        for t in tokens:
            try:
                index = vocab.index(t)
                vector[index] += 1 
            except ValueError:
                continue
        return vector


    def preprocess(self, text: str):
        # Preprocess the text
        tokenizer = nltk.RegexpTokenizer(r"\w+")  # only keep words
        stopwords = nltk.corpus.stopwords.words('english')
        stemmer = nltk.stem.snowball.SnowballStemmer('english')
        newText = tokenizer.tokenize(text)
        newText = [w.lower() for w in newText]
        newText = ["".join([c for c in w if c.isalpha()]) for w in newText]
        newText = [w for w in newText if w not in stopwords]
        newText = [stemmer.stem(w) for w in newText]
        newText = [w for w in newText if any(c.isalpha() for c in w)]
        return newText

    # Loads or downloads the city_description.json file
    def load_city_description(self):
        try:
            with open("city_descriptions.json", 'r') as file:
                city_descriptions = load(file)
        except FileNotFoundError:
            with open("city_descriptions.json", 'w') as file:
                city_descriptions = {}
                for city in self.cities:
                    print(f"Downloading {city}...")
                    city_descriptions[city] = wikipedia.page(city).content
                with open("city_descriptions.json", "w") as file:
                    dump(city_descriptions, file)
        return city_descriptions


    def load_maxtrix_and_bow_and_vocab(self) -> tuple:
        try:
            return (
            numpy.load('tfidf_bow.npy', allow_pickle=True).tolist(),
            numpy.load('vocab.npy', allow_pickle=True).tolist()
            )
        except FileNotFoundError:
            raw_city_descriptions = self.load_city_description()

            # Preprocess the text
            city_descriptions = {}
            for b in raw_city_descriptions:
                city_descriptions[b] = self.preprocess(raw_city_descriptions[b])

            vocabulary = []
            for b in city_descriptions:
                for t in city_descriptions[b]:
                    if t not in vocabulary:
                        vocabulary.append(t)

            # Create book of words vectors
            bow = {}
            for b in city_descriptions:
                bow[b] = self.createVector(vocabulary, city_descriptions[b])

            tfidf_bow = self.tfidf_weighting(bow)
            print(tfidf_bow)

            numpy.save('tfidf_bow.npy', tfidf_bow)
            numpy.save('vocab.npy', vocabulary)
            return (tfidf_bow, vocabulary)


    def sim_cosine(self, vector_1, vector_2):
        similarity = 1 - spatial.distance.cosine(vector_1, vector_2)
        return similarity


    def getMostSimilar(self, description: str, n: int):
        preprocessed_description = self.preprocess(description)
        vector_query = self.createVector(self.vocab, preprocessed_description)
        similarities = {}
        for book in self.bow.keys():
            similarity = self.sim_cosine(self.bow[book], vector_query)
            similarities[book] = similarity
        sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        return [city for (city, sim) in sorted_similarities[:n]]



if __name__ == "__main__":
    ps = PlaceSimilarity()
    text = "beach"
    print(ps.getMostSimilar(text, 3))


