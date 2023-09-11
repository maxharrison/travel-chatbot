
from utils import talk, listen
from classify import Classifier
from name import getName, nameResponse, names_original, get_user_name_response, get_chatbot_name_response
from transactions import bookFlight
from nltk import download
from random import choice


download("stopwords")
download("punkt")
download("averaged_perceptron_tagger")
download("maxent_ne_chunker")
download("words")




def main() -> None:
    intent_classifier = Classifier("intent.json")

    names = names_original()

    talk(f'Hello. My name is {names["chatbot_name"]}.', names)
    talk('I am your personal AI travel agent.', names)
    talk('What is your name?', names)
    
    text = listen(names)

    names["user_name"] = getName(text)
 
    talk(nameResponse(names), names)

    # This variable is used to control the loop
    talking = True

    # Start the main loop
    while talking:

        # Listen for user input and store it in the 'text' variable
        text = listen(names)

        # Use the intent classifier to determine the intent of the user's input
        intent = intent_classifier.classify(text)

        # Check the user's intent and act accordingly
        
        if (intent=="stop"):
            # If the user wants to stop talking, set the 'talking' variable to False to exit the loop
            talking = False
            
        elif (intent=="greeting"):
            # If the user is greeting us, respond with a greeting
            talk("Hi there!", names)

        elif (intent=="how_are_you"):
            responses = ["I am fine thank you", "I am well", "I am good, how are you?"]
            talk(choice(responses), names)

        elif (intent=="i_am_good"):
            responses = ["Excellent", "That is good to hear", "That is great"]
            talk(choice(responses), names)

        elif (intent=="change_name"):
            names["user_name"] = getName(text)
            talk(nameResponse(names), names)
                
        elif (intent=="get_user_name"):
            talk(get_user_name_response(names["user_name"]), names)
                
        elif (intent=="get_chatbot_name"):
            talk(get_chatbot_name_response(names["chatbot_name"]), names)

        elif (intent=="flight"):
            origin, destination, date, return_flight = bookFlight(names)
            talk("Thank you, I will book this now and save the receipt at flights.txt" ,names)
            with open('flights.txt', 'a') as file:
                file.write(f"{origin} -> {destination} @ {date} ({return_flight})\n")
            
        else:
            talk("I don't understand what you mean. Please try again.", names)




if __name__ == "__main__":
    main()