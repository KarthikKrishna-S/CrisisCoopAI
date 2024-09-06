import csv
import random

# Possible entities
foods = ['rice', 'bread', 'eggs', 'milk', 'wheat', 'vegetables', 'fruits', 'meat', 'sugar', 'pulses', 'flour', 'chickpea', 'black channa', 'green gram', 'cowpea', 'dal']
waters = ['water', 'bottled water', 'drinking water', 'well water']
medicines = ['painkillers', 'antibiotics', 'bandages', 'paracetamol', 'tablets', 'Amlodipine', 'Atorvastatin', 'Metformin', 'Albuterol', 'Gabapentin', 'Levothyroxine', 'Amoxicillin', 'Lisinopril', 'Losartan', 'Metoprolol', 'Omeprazole', 'Pantoprazole', 'Sertraline', 'Dextroamphetamine', 'Amphetamine', 'Acetaminophen', 'Hydrocodone', 'Prednisone', 'Rosuvastatin', 'Cephalexin', 'Hydrochlorothiazide', 'Ibuprofen', 'Cyclobenzaprine', 'Montelukast', 'Vitamin D' ,'Acetaminophen']
powers = ['generator', 'electricity', 'solar power', 'battery backup']
shelters = ['tent', 'house', 'apartment', 'shelter']

# Generate a large amount of synthetic data
num_samples = 1000000  # Adjust this number to generate a larger or smaller dataset

with open('synthetic_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['sentence', 'labels'])  # Header

    for _ in range(num_samples):
        sentence = []
        labels = []

        # Randomly choose a number of words to include
        num_words = random.randint(5, 15)

        for i in range(num_words):
            choice = random.choice(['food', 'water', 'medicine', 'power', 'shelter', 'none'])

            if choice == 'food':
                word = random.choice(foods)
                sentence.append(word)
                labels.append('B-FOOD' if i == 0 else 'I-FOOD')
            elif choice == 'water':
                word = random.choice(waters)
                sentence.append(word)
                labels.append('B-WATER' if i == 0 else 'I-WATER')
            elif choice == 'medicine':
                word = random.choice(medicines)
                sentence.append(word)
                labels.append('B-MEDICINE' if i == 0 else 'I-MEDICINE')
            elif choice == 'power':
                word = random.choice(powers)
                sentence.append(word)
                labels.append('B-POWER' if i == 0 else 'I-POWER')
            elif choice == 'shelter':
                word = random.choice(shelters)
                sentence.append(word)
                labels.append('B-SHELTER' if i == 0 else 'I-SHELTER')
            else:
                # Random non-entity words
                non_entity_word = random.choice(['and', 'the', 'with', 'without', 'some', 'many', 'few'])
                sentence.append(non_entity_word)
                labels.append('O')

        # Join sentence into a single string
        sentence_str = ' '.join(sentence)
        labels_str = ' '.join(labels)

        # Write to CSV
        writer.writerow([sentence_str, labels_str])
