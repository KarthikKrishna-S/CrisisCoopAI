import torch
from transformers import BertForTokenClassification, Trainer, TrainingArguments
from data_preparation import load_and_preprocess_data

tags = ['O', 'B-FOOD', 'I-FOOD', 'B-WATER', 'I-WATER', 'B-MEDICINE', 'I-MEDICINE', 
        'B-POWER', 'I-POWER', 'B-SHELTER', 'I-SHELTER']

tag2id = {tag: idx for idx, tag in enumerate(tags)}
id2tag = {idx: tag for tag, idx in tag2id.items()}

def train_model(dataset, model_output_dir='./results'):
    model = BertForTokenClassification.from_pretrained("bert-base-uncased", num_labels=len(tag2id))

    training_args = TrainingArguments(
        output_dir=model_output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
    )
    for data in dataset:
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=data,
        )

        trainer.train()
        model.save_pretrained(model_output_dir)
    return model
