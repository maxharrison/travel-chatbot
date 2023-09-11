
from json import load
from nltk.stem.snowball import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression

# This class Classifier trains a classifier from json dataset file,
# and then classifies text based on these classes.
# This code was heavily inspired and written with Johann Benerradi's lab 3 code example.

class Classifier:
    def __init__(self, filepath: str):
        # Get the data
        data, labels = self.getData(filepath)

        # NLP pipeline

        p_stemmer = PorterStemmer()
        analyzer = CountVectorizer().build_analyzer()

        count_vect = CountVectorizer(
            lowercase=True, stop_words=stopwords.words('english'),
            analyzer=(lambda doc: (p_stemmer.stem(w) for w in analyzer(doc))))
        data_counts = count_vect.fit_transform(data)

        tfidf_transformer = TfidfTransformer(use_idf=True, sublinear_tf=True).fit(data_counts)
        data_tf = tfidf_transformer.transform(data_counts)

        clf = LogisticRegression(random_state=0).fit(data_tf, labels)

        self.count_vect = count_vect
        self.tfidf_transformer = tfidf_transformer
        self.clf = clf


    def getData(self, filepath: str) -> tuple:
        # Generate the training data for the classifier
        data = []
        labels = []
        intent_data = load(open(filepath))
        for intent in intent_data['intents']:
            for text in intent['text']:
                data.append(text)
                labels.append(intent['intent'])
        return (data, labels)


    def classify(self, text: str) -> str:        
        # Preprocessing and creating term-document matrix
        processed_newdata = self.count_vect.transform([text])

        # Weighting
        processed_newdata = self.tfidf_transformer.transform(processed_newdata)

        # Prediction
        return self.clf.predict(processed_newdata)

    