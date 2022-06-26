from azureml.core import Workspace
from azureml.core import Environment
# Model https://docs.microsoft.com/ja-jp/python/api/azureml-core/azureml.core.model.model?view=azure-ml-py#azureml-core-model-model-deploy
from azureml.core.model import Model
# InferenceConfig https://docs.microsoft.com/ja-jp/python/api/azureml-core/azureml.core.model.inferenceconfig?view=azure-ml-py
from azureml.core.model import InferenceConfig
# LocalWebservice https://docs.microsoft.com/ja-jp/python/api/azureml-core/azureml.core.webservice.localwebservice?view=azure-ml-py
from azureml.core.webservice import LocalWebservice

# ワークスペースを取得
workspace = Workspace.from_config()

# デプロイ環境の指定
env = Environment.get(workspace, name="handson-webserver-env")

# 推論構成を定義
inference_config = InferenceConfig(
    environment=env,
    source_directory="src",
    entry_script="handson_model_score.py",
)

# デプロイ条件を指定
deployment_config = LocalWebservice.deploy_configuration(port=6789)

# モデルの取得
model = Model(workspace, name="handson-model")

# デプロイの実施
service = Model.deploy(
    workspace,
    "handson-local-webservice",
    [model],
    inference_config,
    deployment_config,
    overwrite=True,
)
service.wait_for_deployment(show_output=True)