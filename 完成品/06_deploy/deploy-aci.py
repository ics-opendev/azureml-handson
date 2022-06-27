from azureml.core import Environment
from azureml.core.model import InferenceConfig
from azureml.core.model import Model
from azureml.core.webservice import LocalWebservice, AciWebservice
from azureml.core import Workspace

# ワークスペースを取得
ws = Workspace.from_config()

# デプロイ環境の指定
env = Environment.get(ws, name="handson-webserver-env")

# 推論構成を定義
dummy_inference_config = InferenceConfig(
    environment=env,
    source_directory="src",
    entry_script="./handson_model_score.py",
)
# デプロイ条件を指定
deployment_config = AciWebservice.deploy_configuration(
    cpu_cores=0.2, memory_gb=1, auth_enabled=True
)

# モデルの取得
model = Model(ws, name="handson-model")

# デプロイの実施
service = Model.deploy(
    ws,
    "handson-aci-webservice",
    [model],
    dummy_inference_config,
    deployment_config,
    overwrite=True,
)
service.wait_for_deployment(show_output=True)