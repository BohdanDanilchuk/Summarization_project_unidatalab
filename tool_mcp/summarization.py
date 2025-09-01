from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_dir = "BohdanDanylchuk/summarization_model"
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

def summarize_dialog_text(dialog_text: str) -> str:
    inputs = tokenizer(dialog_text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_new_tokens=150)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
