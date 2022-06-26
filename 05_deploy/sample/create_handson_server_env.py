from azureml.core import Workspace
from azureml.core import Environment

# pipから環境を作成
pip_env = Environment.from_pip_requirements('simple-env', 'pip/requirements.txt', pip_version=None)

# ワークスペースを取得
ws = Workspace.from_config()
# 環境をワークスペースに登録
pip_env.register(ws)
