from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset

# Load tokenizer and model
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Load your dataset
dataset = load_dataset("json", data_files="output/dialogpt_finetune_dataset.jsonl", split="train")

# Tokenize the dataset
def tokenize_function(example):
    return tokenizer(example["dialogue"], truncation=True, max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=False)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./dialogpt-finetuned",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    save_steps=500,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=50
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

model.train()
for epoch in range(3):  # 3 epochs
    for batch in train_loader:
        optimizer.zero_grad()
        outputs = model(
            input_ids=batch["input_ids"],
            attention_mask=batch["attention_mask"],
            labels=batch["labels"]
        )
        loss = outputs.loss
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch}: Loss = {loss.item()}")

# Save the final model
trainer.save_model("./dialogpt-finetuned")
tokenizer.save_pretrained("./dialogpt-finetuned")