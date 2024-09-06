from transformers import BertForTokenClassification, BertTokenizer

def load_model_and_tokenizer(model_dir='./fine_tuned_bert'):
    model = BertForTokenClassification.from_pretrained(model_dir)
    tokenizer = BertTokenizer.from_pretrained(model_dir)
    return model, tokenizer

def predict(text, model, tokenizer):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)
    return predictions
