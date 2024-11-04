# runpod-classification

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/repository/docker/dalbodeule/runpod-classification/general) &nbsp; [![GitHub License](https://img.shields.io/github/license/dalbodeule/classification-runpod)
](https://github.com/dalbodeule/classification-runpod?tab=readme-ov-file)

[![CUDA](https://img.shields.io/docker/v/dalbodeule/runpod-classification/cuda?label=cuda)
](https://hub.docker.com/repository/docker/dalbodeule/runpod-classification/tags?name=cuda) &nbsp; [![CPU](https://img.shields.io/docker/v/dalbodeule/runpod-classification/cpu?sort=date&label=CPU)
](https://hub.docker.com/repository/docker/dalbodeule/runpod-classification/tags?name=cpu)

## RunPod Multi-label and Single-label Classification Handler Usage Guide

This code base supports multi-label and single-label classification tasks using Hugging Face models in the RunPod environment. Efficient inference is facilitated with GPU support.

## Environment Setup
Set the `MODEL_NAME` environment variable to specify the model to be used.

```bash
export MODEL_NAME="jioo0224/electra-emotion-korean" # this is a private model
```

Dependencies: Ensure Python, PyTorch, and Transformers libraries are installed.

## Code Overview

- `AutoModelForSequenceClassification` and `AutoTokenizer` are used to load the model and tokenizer based on `MODEL_NAME`.
- The `handler` function processes events from RunPod, takes text inputs in batches, and returns prediction results.
- **Multi-label**: Probabilities are calculated using the `softmax` function.
- **Single-label (binary)**: Probabilities are calculated using the `sigmoid` function.

## Example

### Input Format
```json
{
  "input": {
    "prompt": ["Example text 1", "Example text 2"]
  }
}
```

### Output Format
```json
{
  "predictions": [
    [
      {"label": "label_0", "score": 0.95},
      {"label": "label_1", "score": 0.05}
    ],
    [
      {"label": "label_0", "score": 0.85},
      {"label": "label_1", "score": 0.15}
    ]
  ]
}
```

### Error Handling
- On model loading failure: `"Error loading model {model_name}"`
- If the environment variable is missing: `"MODEL_NAME environment variable is not provided."`
- For input errors: `{"error": "Text is not provided or in the wrong format."}`

This guide and code allow you to run various text classification models seamlessly in RunPod.


## RunPod Multi-label 및 Single-label Classification Handler 사용법

이 코드 베이스는 Hugging Face 모델을 사용하여 RunPod 환경에서 multi-label 및 single-label 분류 작업을 지원합니다. GPU 지원을 통해 효율적인 추론을 수행할 수 있습니다.

## 환경 설정
환경 변수 설정: MODEL_NAME 환경 변수를 설정하여 사용할 모델 이름을 지정합니다.

```bash
코드 복사
export MODEL_NAME="jioo0224/electra-emotion-korean" # this is private model
```
의존성: Python 및 PyTorch, Transformers 라이브러리가 설치되어 있어야 합니다.

## 코드 설명

- AutoModelForSequenceClassification과 AutoTokenizer는 MODEL_NAME에 따라 모델과 토크나이저를 로드합니다.
- handler 함수는 RunPod의 이벤트를 처리하며, 배치 단위로 텍스트를 입력받아 예측 결과를 반환합니다.
- Multi-label: 각 클래스에 대한 확률을 softmax를 사용해 계산.
- Single-label (binary): sigmoid 함수로 확률 계산.

## 예제

### 입력 형식
```json
{
  "input": {
    "prompt": ["Example text 1", "Example text 2"]
  }
}
```
출력 형식
```json
{
  "predictions": [
    [
      {"label": "label_0", "score": 0.95},
      {"label": "label_1", "score": 0.05}
    ],
    [
      {"label": "label_0", "score": 0.85},
      {"label": "label_1", "score": 0.15}
    ]
  ]
}
```
### 에러 처리
- 모델 로드 실패 시: "Error loading model {model_name}"
- 환경 변수 누락 시: "MODEL_NAME environment variable is not provided."
- 입력 오류 시: {"error": "Text is not provided or in the wrong format."}