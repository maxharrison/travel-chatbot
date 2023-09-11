

months = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

def dateParser(text):
    # format of date: dd-mm-yyyy
    day = int(text[0:2])
    month = int(text[3:5])
    year = int(text[6:10])

    return f"{day} / {months[month]} / {year}"

