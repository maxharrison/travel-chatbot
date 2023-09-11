# Named Entity Recognition

# Named entities are definite noun phrases that refer to specific types of individuals,
# such as organizations, persons, dates, and so on.

# nltk.org/book/ch07.html
# some of the code was inspired by this webpage, but I didn't copy any of it line for line

import nltk


def tag(text):
    # Tokenize and tag each token with their part-of-speech
    words = nltk.word_tokenize(text)
    return nltk.pos_tag(words)



def getNamedEntity(entity, text):
    # Convert the text to lowercase and capitalize the first letter of each word
    text = text.lower()
    text = text.title()

    # Tokenize and tag each token with their part-of-speech
    tagged_words = tag(text)

    # Use NLTK's named entity chunker to identify named entities in the text, and return the tree
    tree = nltk.ne_chunk(tagged_words)

    # Traverse the tree to identify the specified entity label
    for subtree in tree.subtrees():
        if subtree.label() == entity:
             # Return the first word in the subtree
            return subtree.leaves()[0][0]

    # If no named entity of the specified type is found, return the first word of the text, capitalized.
    return text.split()[0].capitalize()

