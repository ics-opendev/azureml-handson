import requests
import json
from azureml.core import Workspace
from azureml.core.webservice import LocalWebservice

# ワークスペースを取得
ws = Workspace.from_config()

# 実行中のWebサービスを取得
service = LocalWebservice(workspace=ws, name="handson-local-webservice")

# エンドポイントを取得
scoring_uri = service.scoring_uri

# 画像を添付
files = {'image': open('./testdata_cifar10/1/32.jpg', 'rb').read()}

# リクエストを実行
response = requests.post(scoring_uri, files=files)

print(response.json())