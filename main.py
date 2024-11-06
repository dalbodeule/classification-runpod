import runpod
import torch
import os
import json
import asyncio
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# 모델과 토크나이저 로드
def load_model():
    model_name = os.getenv("MODEL_NAME", "")
    if not model_name:
        return json.dumps({"error": "MODEL_NAME env is not provided."})
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
    except Exception as e:
        return json.dumps({"error": f"Error loading model {model_name}: {str(e)}"})
    return model, tokenizer

# 각 텍스트 검증 및 예측을 수행하는 비동기 함수
async def process_text(model, tokenizer, text, device):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Process outputs
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=-1).tolist()
    labels = model.config.id2label
    
    result = [{"label": labels[i], "score": score} for i, score in enumerate(probabilities[0])]
    return result

# 핸들러 함수
async def handler(job):
    global tokenizer
    global model
    
    # 모델과 토크나이저가 없으면 로드
    if 'model' not in globals() or 'tokenizer' not in globals():
        model, tokenizer = load_model()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    
    input_data = job.get("input", {})
    texts = input_data.get("prompt", [])  # Batch inputs
    
    if not texts or not isinstance(texts, list):
        return json.dumps({"error": "Texts are not provided or in the wrong format."})
    
    # 비동기적으로 모든 텍스트 처리
    results = await asyncio.gather(*(process_text(model, tokenizer, text, device) for text in texts))
    
    return json.dumps({"predictions": results})

# RunPod 서버리스 인퍼런스 시작
runpod.serverless.start({
    "handler": handler
})