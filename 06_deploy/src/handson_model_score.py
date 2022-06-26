import numpy as np
import json
import os
import torch
import torch.nn as nn
from torchvision import transforms
from model import Net
from PIL import Image
from azureml.contrib.services.aml_request import AMLRequest, rawhttp
from azureml.contrib.services.aml_response import AMLResponse

# タグ
classes = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

def init():
    global model
    # ネットワークの読み込み
    model = Net()
    # 学習済みモデルのパスを取得
    model_path = os.path.join(os.getenv("AZUREML_MODEL_DIR"), "model.pth")
    # 読み込み
    model.load_state_dict(torch.load(model_path))

@rawhttp
def run(request):
    # POST以外は受け付けない
    if request.method != 'POST':
        return AMLResponse("bad request", 500)
    
    # 画像を取得
    file_bytes = request.files["image"]

    # 前処理
    image_tensor = preprocess(file_bytes)

    # 推論を実行
    with torch.no_grad():
        # 推論
        outputs = model(image_tensor)
        # scoreを算出
        softmax = nn.Softmax(dim=1)
        pred_probs = softmax(outputs.data).numpy()[0]
        # 最大スコアのindexを取得
        index = torch.argmax(outputs.data, 1)

    # 推論結果
    result = {'target': str(classes[index]), 'score': str(pred_probs[index])}
    return result
    
def preprocess(file_bytes):
    data_transforms = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    image = Image.open(file_bytes).convert('RGB')
    image = data_transforms(image).float()
    image = torch.tensor(image)
    image = image.unsqueeze(0)
    return image