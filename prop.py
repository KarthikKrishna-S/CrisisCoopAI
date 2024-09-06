from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("chambliss/distilbert-for-food-extraction")
model = AutoModelForTokenClassification.from_pretrained("chambliss/distilbert-for-food-extraction")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)
example = "We currently have 20 kg of rice, 15 liters of water, and enough power to last 3 days. Additionally, we possess 5 kg of wheat flour, 10 kg of sugar, and 12 kg of pulses. There's also a supply of 30 liters of milk, 10 kg of vegetables, 5 kg of fruits, and 2 kg of meat. Our medicine cabinet contains a bottle of paracetamol with 30 tablets, 20 capsules of antibiotics, and 10 strips of bandages. We've also got 5 bottles of hand sanitizer, 3 packs of face masks, and 2 liters of disinfectant solution. Unfortunately, our power supply is unstable, and we might lose electricity in the next 2 days. We do have a small generator that can run for 4 hours a day, but fuel is limited to just 10 liters. As for shelter, our house is sturdy, but it might not withstand a severe storm. Regarding food, we also have 15 kg of potatoes, 6 kg of onions, 3 kg of tomatoes, 5 packets of instant noodles, 10 cans of beans, 8 cans of soup, and 20 packets of biscuits. We’ve got 3 loaves of bread, 5 dozen eggs, and 3 kg of cheese.  Water-wise, we've stored 50 liters in bottles, 100 liters in tanks, and 20 liters in buckets. There\'s also 10 liters of juice, 5 liters of soft drinks, and 2 liters of milk remaining. We’re also running low on painkillers, with only 10 tablets of ibuprofen left. Our first aid kit contains some basic supplies, but nothing for serious injuries. In terms of power, we\'ve managed to charge 2 battery packs and 3 flashlights, but they won\'t last long. Shelter is not an issue for now, but we\'re concerned about the integrity of the roof during heavy rains. We've also got 5 kg of pasta, 10 kg of rice, 2 kg of dried beans, and 6 liters of cooking oil. For water, there\'s 40 liters left, but we\’re unsure of its quality. The medicine situation is getting critical as we only have a few antibiotics and no more inhalers for asthma. Lastly, power remains a challenge with just 3 more days of electricity if usage is limited."

ner_results = nlp(example)
print(ner_results)
for i in ner_results:
    if i['entity'] == 'LABEL_0' and i['score']>0.9:
        print(i)