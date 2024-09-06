from data_preparation import load_and_preprocess_data
from model_training import train_model
from inference import load_model_and_tokenizer, predict
from transformers import BertTokenizerFast
import torch
from torch.utils.data import Dataset

class CustomNERDataset(Dataset):
    def __init__(self, tokenized_texts_and_labels, tokenizer, max_len=128):
        self.tokenized_texts_and_labels = tokenized_texts_and_labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.tokenized_texts_and_labels)

    def __getitem__(self, index):
        tokenized_sentence, labels = self.tokenized_texts_and_labels[index]

        # Convert tokens to input IDs, attention masks, etc.
        input_ids = self.tokenizer.convert_tokens_to_ids(tokenized_sentence)
        attention_mask = [1] * len(input_ids)

        # Convert labels from strings to ids
        label_ids = [tag2id.get(label, -100) for label in labels]  # Default to -100 if label is not in tag2id

        # Padding to max_len
        padding_length = self.max_len - len(input_ids)
        input_ids = input_ids + ([self.tokenizer.pad_token_id] * padding_length)
        attention_mask = attention_mask + ([0] * padding_length)
        label_ids = label_ids + ([-100] * padding_length)  # Use -100 to ignore in loss calculation

        # Debug print statements
        print(f"Tokenized Sentence: {tokenized_sentence}")
        print(f"Labels: {labels}")
        print(f"Label IDs: {label_ids}")

        return {
            'input_ids': torch.tensor(input_ids, dtype=torch.long),
            'attention_mask': torch.tensor(attention_mask, dtype=torch.long),
            'labels': torch.tensor(label_ids, dtype=torch.long)  # Ensure this is a list of integers
        }

tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")

# Example input tokens and labels
tokens = ['rice', 'bread', 'eggs', 'milk', 'wheat', 'vegetables', 'fruits', 'meat', 'sugar', 'pulses', 'flour', 'chickpea', 'black channa', 'green gram', 'cowpea', 'dal', 'water', 'bottled water', 'drinking water', 'well water', 'painkillers', 'antibiotics', 'bandages', 'paracetamol', 'tablets', 'Amlodipine', 'Atorvastatin', 'Metformin', 'Albuterol', 'Gabapentin', 'Levothyroxine', 'Amoxicillin', 'Lisinopril', 'Losartan', 'Metoprolol', 'Omeprazole', 'Pantoprazole', 'Sertraline', 'Dextroamphetamine', 'Amphetamine', 'Acetaminophen', 'Hydrocodone', 'Prednisone', 'Rosuvastatin', 'Cephalexin', 'Hydrochlorothiazide', 'Ibuprofen', 'Cyclobenzaprine', 'Montelukast', 'Vitamin D', 'Acetaminophen', 'generator', 'electricity', 'solar power', 'battery backup', 'tent', 'house', 'apartment', 'shelter']
labels = ['I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-FOOD', 'I-WATER', 'I-WATER', 'I-WATER', 'I-WATER', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-MEDICINE', 'I-POWER', 'I-POWER', 'I-POWER', 'I-POWER', 'I-SHELTER', 'I-SHELTER', 'I-SHELTER', 'I-SHELTER']

# Tokenize the inputs
encoding = tokenizer(tokens, is_split_into_words=True, return_offsets_mapping=True, padding=True, truncation=True, return_tensors="pt")

tags = ['O', 'B-FOOD', 'I-FOOD', 'B-WATER', 'I-WATER', 'B-MEDICINE', 'I-MEDICINE', 
        'B-POWER', 'I-POWER', 'B-SHELTER', 'I-SHELTER']

# Create tag2id (tag to numerical ID) and id2tag (ID to tag) mappings
tag2id = {tag: idx for idx, tag in enumerate(tags)}
id2tag = {idx: tag for tag, idx in tag2id.items()}

def align_labels_with_tokens(tokenized_inputs, word_labels):
    labels = []
    word_ids = tokenized_inputs.word_ids()  # Get the word ids (which word each token belongs to)
    
    previous_word_idx = None
    label_ids = []
    
    for word_idx in word_ids:
        if word_idx is None:  # Token corresponds to special tokens like [CLS] or [SEP]
            label_ids.append(-100)  # Ignore the special tokens
        elif word_idx != previous_word_idx:  # New word, take the corresponding label
            label_ids.append(tag2id[word_labels[word_idx]])
        else:  # Same word as before, repeat the label
            label_ids.append(tag2id[word_labels[word_idx]])
        previous_word_idx = word_idx

    return label_ids

aligned_labels = align_labels_with_tokens(encoding, labels)
aligned_labels_tensor = torch.tensor(aligned_labels, dtype=torch.long)
encoding["labels"] = aligned_labels_tensor

class CustomDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings  # Tokenized inputs
        self.labels = labels        # Aligned labels
    
    def __getitem__(self, idx):
        # Get the item at index `idx` from the tokenized encodings
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        # Add the aligned labels
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    
    def __len__(self):
        return len(self.labels)

# Prepare dataset
dataset = CustomDataset(encoding, aligned_labels)



from torch.utils.data import DataLoader

# Step 1: Prepare the data (continuation from the previous example)
tokenized_texts_and_labels, tokenizer = load_and_preprocess_data("synthetic_data.csv")

# Step 2: Create a dataset instance
dataset = CustomNERDataset(tokenized_texts_and_labels, tokenizer)

# Step 3: Create a DataLoader for batching
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

# Step 4: Train the model using the DataLoader
model = train_model(dataloader)

model.save_pretrained("./fine_tuned_bert")
tokenizer.save_pretrained("./fine_tuned_bert")

# # Step 3: Make predictions
# model, tokenizer = load_model_and_tokenizer()
# text = "I have 10 kg of rice and 5 liters of water."
# predictions = predict(text, model, tokenizer)
# print(predictions)
