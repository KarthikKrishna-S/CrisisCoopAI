foods = ['rice', 'bread', 'eggs', 'milk', 'wheat', 'vegetables', 'fruits', 'meat', 'sugar', 'pulses', 'flour', 'chickpea', 'black channa', 'green gram', 'cowpea', 'dal']
waters = ['water', 'bottled water', 'drinking water', 'well water']
medicines = ['painkillers', 'antibiotics', 'bandages', 'paracetamol', 'tablets', 'Amlodipine', 'Atorvastatin', 'Metformin', 'Albuterol', 'Gabapentin', 'Levothyroxine', 'Amoxicillin', 'Lisinopril', 'Losartan', 'Metoprolol', 'Omeprazole', 'Pantoprazole', 'Sertraline', 'Dextroamphetamine', 'Amphetamine', 'Acetaminophen', 'Hydrocodone', 'Prednisone', 'Rosuvastatin', 'Cephalexin', 'Hydrochlorothiazide', 'Ibuprofen', 'Cyclobenzaprine', 'Montelukast', 'Vitamin D' ,'Acetaminophen']
powers = ['generator', 'electricity', 'solar power', 'battery backup']
shelters = ['tent', 'house', 'apartment', 'shelter']
print(len(foods), len(waters), len(medicines), len(powers), len(shelters))
print(foods+waters+medicines+powers+shelters)

tokens = []

for i in foods:
    tokens.append("I_FOOD")
for i in waters:
    tokens.append("I_WATER")
for i in medicines:
    tokens.append("I_MEDICINE")
for i in powers:
    tokens.append("I_POWER")
for i in shelters:
    tokens.append("I_SHELTER")
print(tokens)