import requests
import json
from azureml.core import Workspace
from azureml.core import LocalWebservice

# ワークスペースを取得
ws = Workspace.from_config()

# 実行中のWebサービスを取得
service = LocalWebservice(workspace=ws, name="handson-local-webservice")
# エンドポイントを取得
scoring_uri = service.scoring_uri

headers = {"Content-Type": "application/json"}
data = {
    "query": "Query",
    "context": "Context",
}
data = json.dumps(data)
response = requests.post(uri, data=data, headers=headers)
print(response.json())