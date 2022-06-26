import requests
import json
from azureml.core import Workspace
from azureml.core.webservice import Webservice

# ワークスペースを取得
ws = Workspace.from_config()

# 実行中のWebサービスを取得
service = Webservice(workspace=ws, name="handson-aci-webservice")

# エンドポイントを取得
scoring_uri = service.scoring_uri

# 認証キーを取得
key, _ = service.get_keys()

# 認証ヘッダーを追加
headers = {"Authorization": f"Bearer {key}"}

# 画像を添付
files = {'image': open('../testdata_cifar10/automobile/32.jpg', 'rb').read()}

# リクエストを実行
response = requests.post(scoring_uri, files=files, headers=headers)
print(response.json())