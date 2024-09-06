import pandas as pd
from transformers import BertTokenizer

def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    tokenizer = BertTokenizer.from_pretrained("chambliss/distilbert-for-food-extraction")
    
    def tokenize_and_preserve_labels(sentence, text_labels):
        tokenized_sentence = []
        labels = []

        for word, label in zip(sentence.split(), text_labels):
            tokenized_word = tokenizer.tokenize(word)
            tokenized_sentence.extend(tokenized_word)
            labels.extend([label] * len(tokenized_word))

        return tokenized_sentence, labels
    
    tokenized_texts_and_labels = [
        tokenize_and_preserve_labels(sent, labs) 
        for sent, labs in zip(df['sentence'].values, df['labels'].values)
    ]
    
    return tokenized_texts_and_labels, tokenizer
