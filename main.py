import runpod
import torch
import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load model and tokenizer outside the handler
model_name = os.getenv("MODEL_NAME", "")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Set model to evaluation mode
model.eval()

def handler(event):
    # Extract text from the event
    input_data = event.get("input", {})
    texts = input_data.get("prompt", [])

    if not texts or not isinstance(texts, list):
        return {"error": "text is not provided or wrong format."}

    # Tokenize and prepare input for batch
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True).to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Process outputs for batch
    logits = outputs.logits
    probabilities_batch = torch.softmax(logits, dim=1)

    # Prepare results for multi-label classification for each input
    results = []
    for probs in probabilities_batch:
        results.append([{"label": f"label_{i}", "score": float(prob)} for i, prob in enumerate(probs)])

    return {"predictions": results}

# Start RunPod serverless inference
runpod.serverless.start({"handler": handler})