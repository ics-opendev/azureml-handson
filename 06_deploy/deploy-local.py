from azureml.core import Workspace
from azureml.core import Environment
from azureml.core.model import Model
from azureml.core.model import InferenceConfig
from azureml.core.webservice import LocalWebservice

# ワークスペースを取得
workspace = Workspace.from_config()

# デプロイ環境の指定
env = Environment.get(workspace, name="handson-webserver-env")

# 推論構成を定義
inference_config = InferenceConfig(
    environment=env,
    source_directory="",
    entry_script="",
)

# デプロイ条件を指定
deployment_config = LocalWebservice.deploy_configuration(port=6789)


# デプロイの実施
service = Model.deploy(
    workspace,
    "handson-local-webservice",
    [],
    inference_config,
    deployment_config,
    overwrite=True,
)
service.wait_for_deployment(show_output=True)