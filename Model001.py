import spacy
import ast

adultf = 2250
childf = 1400
adultw = 3
childw = 2

nlp = spacy.load("en_core_web_trf")

fdb = {
    "rice": 3640,  # calories per kg
    "beans": 3470,
    "wheat": 3400,
    "potato": 770,
    "apple": 520,
    "banana": 890,
    "chicken breast": 1650,
    "beef steak": 2500,
    "salmon": 2060,
    "tofu": 760,
    "egg": 1550,
    "milk": 640,
    "yogurt": 600,
    "cheddar cheese": 4030,
    "butter": 7170,
    "olive oil": 8840,
    "peanut butter": 5890,
    "almonds": 5790,
    "walnuts": 6540,
    "carrot": 410,
    "broccoli": 340,
    "spinach": 230,
    "tomato": 180,
    "grapes": 690,
    "orange": 470,
    "strawberry": 320,
    "avocado": 1600,
    "quinoa": 3680,
    "couscous": 3760,
    "oats": 3890,
    "barley": 3400,
    "corn": 3650,
    "sweet potato": 860,
    "chickpeas": 1640,
    "lentils": 1160,
    "mushrooms": 220,
    "pasta": 3710,
    "bread": 2500,
    "honey": 3040,
    "sugar": 4000,
    "flour": 3640,
    "channa": 3780,
    "green gram": 3470,
    "dal": 1040,
    "bitter gourd": 170,
    "brinjal": 250,
    "cabbage": 250,
    "carrot": 410,
    "cauliflower": 250,
    "chili pepper": 400,
    "cucumber": 160,
    "drumstick": 300,
    "ladyfinger": 330,
    "long beans": 230,
    "pumpkin": 260,
    "snake gourd": 230,
    "tomato": 180,
    "ash gourd": 130,
    "elephant yam": 1500,
    "raw banana": 1300,
    "coriander leaves": 250,
    "spinach": 230,
    "green peas": 810,
    "beetroot": 430,
    "sweet potato": 860,
    "broad beans": 340,
    "taro root": 720,
    "amaranth leaves": 230,
    "kolkhoz": 120,
    "yam": 1180,
    "sorrel leaves": 80,
    "kohlrabi": 280,
    "radish": 150,
    "zuccini": 170,
    "banana": 890,
    "mango": 700,
    "papaya": 430,
    "pineapple": 500,
    "guava": 680,
    "orange": 470,
    "apple": 520,
    "grapes": 690,
    "watermelon": 300,
    "coconut": 3540,
    "jackfruit": 950,
    "pomegranate": 830,
    "soursop": 660,
    "starfruit": 310,
    "avocado": 1600,
    "chickoo": 830,
    "custard apple": 300,
    "dragon fruit": 600,
    "lychee": 660,
    "rambutan": 680,
    "passion fruit": 970,
    "grapefruit": 420,
    "date palm": 2770,
    "kiwi": 610,
    "strawberry": 320,
    "blueberry": 570

}


def extract_resources(na ,nc ,doc):

    print(doc)
    print(doc)

    wfl = 0
    ffl = 0

    resources = {
        "water": None,
        "food": None,
        "power": None,
        "medicine": None,
        "shelter": None
    }
    calcres = {
        "water": None,
        "food": None,
        "power": None
    }
    
    for token in doc:
        if token.is_digit:
            valu = int(token.text)
            print(token)
            quantity = float(token.text)
            next_token = token.nbor(1) 
            next2_token = token.nbor(2)
            next3_token = token.nbor(3)
            next4_token = token.nbor(4)

            if "gallon" in (next_token.text.lower() or next2_token.text.lower()):
                calcres["water"] = quantity * 3.785  
            elif "litre" in (next_token.text.lower() or next2_token.text.lower()):
                calcres["water"] = quantity
            elif "day" in next_token.text.lower() or "week" in next_token.text.lower():
                if "food" in (next2_token.text.lower() or next3_token.text.lower() or next4_token.text.lower()):
                    ffl = 1
                    resources["food"] = quantity
                elif "water" in (next2_token.text.lower() or next3_token.text.lower() or next4_token.text.lower()):
                    wfl = 1
                    resources["water"] = quantity
            elif "can" in next_token.text.lower():
                calcres["food"] = (calcres["food"] or 0) + quantity * 100  
            elif ("kg" or "kilogram") in next_token.text.lower():
                if (str(next2_token.text.lower())+" "+str(next3_token.text.lower())) in fdb or next_token.text.lower() in fdb:
                    calcres["food"] = (calcres["food"] or 0) + (fdb[str(next2_token.text.lower())+" "+str(next3_token.text.lower())]*valu)
                elif (str(next3_token.text.lower())+" "+str(next4_token.text.lower())) in fdb or next_token.text.lower() in fdb:
                    calcres["food"] = (calcres["food"] or 0) + (fdb[str(next3_token.text.lower())+" "+str(next4_token.text.lower())]*valu)
                elif next2_token.text.lower() in fdb or next_token.text.lower() in fdb:
                    calcres["food"] = (calcres["food"] or 0) + (fdb[next2_token.text.lower()]*valu)
                elif next3_token.text.lower() in fdb or next_token.text.lower() in fdb:
                    calcres["food"] = (calcres["food"] or 0) + (fdb[next3_token.text.lower()]*valu)
                elif next4_token.text.lower() in fdb or next_token.text.lower() in fdb:
                    calcres["food"] = (calcres["food"] or 0) + (fdb[next4_token.text.lower()]*valu)
                print(calcres["food"])
            elif ("g" or "gram") in next_token.text.lower():
                if (str(next2_token.text.lower())+" "+str(next3_token.text.lower())) in fdb or next_token.text.lower() in fdb:
                    calcres["food"] = (calcres["food"] or 0) + ((fdb[str(next3_token.text.lower())+" "+str(next4_token.text.lower())]*valu)/1000)
                elif (str(next3_token.text.lower())+" "+str(next4_token.text.lower())) in fdb or next_token.text.lower() in fdb:
                    calcres["food"] = (calcres["food"] or 0) + ((fdb[str(next3_token.text.lower())+" "+str(next4_token.text.lower())]*valu)/1000)
                elif next2_token.text.lower() in fdb or next_token.text.lower() in fdb:
                    calcres["food"] = (calcres["food"] or 0) + ((fdb[next2_token.text.lower()]*valu)/1000)
                elif next3_token.text.lower() in fdb or next_token.text.lower() in fdb:
                    calcres["food"] = (calcres["food"] or 0) + ((fdb[next3_token.text.lower()]*valu)/1000)
                elif next4_token.text.lower() in fdb or next_token.text.lower() in fdb:
                    calcres["food"] = (calcres["food"] or 0) + ((fdb[next4_token.text.lower()]*valu)/1000)


        elif token.text.lower() == "no":
            following_token = token.nbor(1).text.lower()
            if following_token == "power":
                resources["power"] = 7  # Default to 7 days without power
            elif following_token == "shelter":
                resources["shelter"] = 3  # Default to 3 days without shelter
            elif following_token == "medicine":
                resources["medicine"] = 7  # Default to 7 days without medicine
        elif token.text.lower() == "ok":
            if "shelter" in [t.text.lower() for t in doc]:
                resources["shelter"] = float('inf')  # Infinite shelter (assumed adequate)
        
    if wfl == 0:
        if calcres["water"] != None:
            resources["water"] = (calcres["water"]or 0)/int((((na or 0)*adultw)+((nc or 0)*childw)))
    if ffl == 0:
        if calcres["food"] != None:
            resources["food"] = calcres["food"]/(((na or 0)*adultf)+((nc or 0)*childf))

    print(resources)
    days = []
    for i in resources.values():
        if i != None:
            days.append(i)
    print(days)
    return days


def process(data):
    output = []
    output.append(data[0])
    output.append(data[1]+data[2])
    output.append(min(extract_resources(data[1], data[2], nlp(data[3]))))
    print(min(extract_resources(data[1], data[2], nlp(data[3]))))

    return output

def confile(filename1, filename2):
    print("ran")
    input = []
    output = []
    with open(filename1, "r") as inp:
        uncinp = []
        a = inp.readlines()
        uncinp.append(a)
        for j in uncinp:
            for i in j:
                x = ast.literal_eval(i)
                input.append(x)
    
    for i in input:
        output.append(process(i))
    
    with open(filename2, "w") as out:
        out.writelines(str(output))


confile("input.txt", "output.txt")