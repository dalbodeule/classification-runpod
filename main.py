import runpod
import torch
import os
import json
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def load_model():
    # Load model and tokenizer outside the handler
    model_name = os.getenv("MODEL_NAME", "")

    if not model_name:
        return json.dumps({ "error": "MODEL_NAME env is not provided."})

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
    except Exception as e:
        return json.dumps({ "error": f"Error loading model {model_name}: {str(e)}"})

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
        return json.dumps({"error": "Text is not provided or in the wrong format."})

    # Tokenize and prepare input for batch
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True).to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Process outputs for batch
    logits = outputs.logits

    # Get the label mapping
    labels = model.config.id2label # Retrieves the vocabulary, but you may need a specific mapping
    label_list = list(labels.keys())  # or your specific label mapping

    # Prepare results
    results = []
    for logit in logits:
        probabilities = torch.softmax(logit, dim=-1).tolist()
        result = [{"label": label_list[i], "score": score} for i, score in enumerate(probabilities)]
        results.append(result)

    return json.dumps({"predictions": results})

# Start RunPod serverless inference
runpod.serverless.start({
    "handler": handler
})