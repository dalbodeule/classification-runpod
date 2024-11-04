import runpod
import torch
import os
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def load_model():
    # Load model and tokenizer outside the handler
    model_name = os.getenv("MODEL_NAME", "")

    if not model_name:
        return { "error": "MODEL_NAME env is not provided."}

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
    except Exception as e:
        return { "error": f"Error loading model {model_name}: {str(e)}"}

    return (model, tokenizer)

def handler(job):
    global tokenizer
    global model

    if 'model' not in globals() or 'tokenizer' not in globals():
        model, tokenizer = load_model()
    
    # Move model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Set model to evaluation mode
    model.eval()

    # Extract text from the event
    input_data = job.get("input", {})
    texts = input_data.get("prompt", [])

    if not texts or not isinstance(texts, list):
        yield {"error": "Text is not provided or in the wrong format."}

    # Tokenize and prepare input for batch
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True).to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Process outputs for batch
    logits = outputs.logits

    if logits.shape[1] > 1:  # Multi-label or single-label classification
        probabilities_batch = torch.softmax(logits, dim=1)
        results = []
        for idx, probs in enumerate(probabilities_batch):
            runpod.serverless.progress_update(job, f"Updated {idx + 1}/{len(texts)}")
            results.append([{ "label": f"label_{i}", "score": float(prob) } for i, prob in enumerate(probs)])
    else:  # Binary classification case
        probabilities_batch = torch.sigmoid(logits)
        results = []
        for idx, prob in enumerate(probabilities_batch):
            runpod.serverless.progress_update(job, f"Updated {idx + 1}/{len(texts)}")
            results.append([{ "label": "positive", "score": float(prob) }, { "label": "negative", "score": 1.0 - float(prob) }])

    return {"predictions": results}

# Start RunPod serverless inference
runpod.serverless.start({
    "handler": handler
})