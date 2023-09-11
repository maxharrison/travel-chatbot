import spacy

from ner import getNamedEntity

nlp = spacy.load("en_core_web_sm")

def scapyner(entity, text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == entity:
            return ent.text


data = [
    ("max", "max"),
    ("max is my name", "max"),
    ("my name is max", "max"),
    ("call me max", "max") , 
    ("i go by max", "max"),
    ("im max", "Max"),
    ("you can call me max", "Max"),
    ("max is my name", "Max"),
    ("Michael", "Michael"),
    ("Michael is my name", "Michael"),
    ("my name is Michael", "Michael"),
    ("call me Michael", "Michael") ,
    ("i go by Michael", "Michael"),
    ("im Michael", "Michael"),
    ("you can call me Michael", "Michael"),
    ("Michael is my name", "Michael"),
    ("Emily", "Emily"),
    ("Emily is my name", "Emily"),
    ("my name is Emily", "Emily"),
    ("call me Emily", "Emily") ,
    ("i go by Emily", "Emily"),
    ("im Emily", "Emily"),
    ("you can call me Emily", "Emily"),
    ("Emily is my name", "Emily"),
    ("Joshua", "Joshua"),
    ("Joshua is my name", "Joshua"),
    ("my name is Joshua", "Joshua"),
    ("call me Joshua", "Joshua") ,
    ("i go by Joshua", "Joshua"),
    ("im Joshua", "Joshua"),
    ("you can call me Joshua", "Joshua"),
    ("Joshua is my name", "Joshua"),
    ("Madison", "Madison"),
    ("Madison is my name", "Madison"),
    ("my name is Madison", "Madison"),
    ("call me Madison", "Madison") ,
    ("i go by Madison", "Madison"),
    ("im Madison", "Madison"),
    ("you can call me Madison", "Madison"),
    ("Madison is my name", "Madison")
]




my_ner = 0
scapy_ner = 0

for text, name in data:
    name = name.lower()
    try:
        if getNamedEntity("PERSON", text).lower() == name:
            my_ner += 1
    except:
        continue
    try:
        if scapyner("PERSON", text).lower() == name:
            scapy_ner += 1
    except:
        continue



import matplotlib.pyplot as plt

# create the values to plot
values = [my_ner, scapy_ner]

# Define the labels for the bars
labels = ["ALEX", "spaCy"]

# Create the bar chart
plt.bar(labels, values)

# Add a title
plt.title("Number of correct named entity extractions")

# Label the y-axis
plt.ylabel("Number of correct extractions")

# Set the y-axis range
plt.ylim(0, 40)

# Show the plot
plt.show()

#plt.savefig("ner_graph.png")




import matplotlib.pyplot as plt
import numpy as np


labels = ['ALEX', 'Google']
user_1_score = [6, 5]
user_2_score = [7, 6]
user_3_score = [7, 4]
user_4_score = [9, 5]

x = np.arange(len(labels))  # the label locations
width = 0.25  # the width of the bars

fig, ax = plt.subplots()

rects3 = ax.bar(x - width, user_3_score, width/2, label='User 1')
rects1 = ax.bar(x - width*(0.33), user_1_score, width/2, label='User 2')
rects2 = ax.bar(x + width*(0.33), user_2_score, width/2, label='User 3')
rects4 = ax.bar(x + width, user_4_score, width/2, label='User 4')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Satisfaction out of 10')
ax.set_title('Do users prefer using Alex or Google for destination recommendation')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)
ax.bar_label(rects4, padding=3)


fig.tight_layout()

plt.ylim(0, 10)

plt.show()

#plt.savefig("destination_graph.png")
