
import ner

from utils import talk, listen
from name import names_original
from classify import Classifier
from date import dateParser
from place_similarity import PlaceSimilarity




def bookFlight(names):
    yesno_classifier = Classifier("yesno.json")
    placeSimilarity = PlaceSimilarity()

    talk("Do you know where you would like to go?", names)
    answer = yesno_classifier.classify(listen(names))
    if answer == "yes":
        talk("What is the name of the city you would like to go?", names)
        destination = askCityName(names, yesno_classifier)
    else:
        talk("Thats okay I will help you find your perfect destination", names)
        destination = askCityQuestions(names, yesno_classifier, placeSimilarity)

    talk("What is the name of the city you would like to depart from?", names)
    origin = askCityName(names, yesno_classifier)

    talk("What is the date you like to depart? (DD-MM-YYYY)", names)
    date = dateParser(listen(names))

    talk("Finally, would you like to book this as a return flight?", names)
    answer = yesno_classifier.classify(listen(names))
    if answer == "yes":
        return_flight = "return"
    else:
        return_flight = "one-way"

    talk(f"Thank you very much. So I will book a {return_flight} flight from {origin}, flying to {destination} on {date}.", names)

    talk("Is this correct?", names)
    answer = yesno_classifier.classify(listen(names))
    if answer == "yes":
        return (origin, destination, date, return_flight)
    else:
        talk("Okay, let's try again", names)
        return bookFlight(names)
    

def askCityQuestions(names, yesno_classifier, placeSimilarity):
    talk(f"Please can you describe your ideal destination for me?", names)
    descriptions = listen(names)
    cities = placeSimilarity.getMostSimilar(descriptions, 3)
    
    talk(f"I have found a few cities that meet this criteria", names)
    talk(f"{cities[0]} would be my first choice, then {cities[1]} would be my second choice, but {cities[2]} wouldn't be far behind", names)

    talk(f"Which one would you like to choose?", names)
    return askCityName(names, yesno_classifier)



def askCityName(names, yesno_classifier):
    city = ner.getNamedEntity("GPE", listen(names))
    talk(f"Is {city} the correct city?", names)
    answer = yesno_classifier.classify(listen(names))
    if answer == "yes":
        talk("Okay brilliant!", names)
        return city
    else:
        talk("Okay, try wording your answer differently", names)
        return askCityName(names, yesno_classifier)


if __name__ == "__main__":
    bookFlight()