from azureml.core import Workspace
from azureml.core import Environment

# pipから環境を作成
pip_env = Environment.from_pip_requirements('handson-webserver-env', 'pip/requirements.txt', pip_version=None)

# ワークスペースを取得
workspace = Workspace.from_config()
# 環境をワークスペースに登録
pip_env.register(workspace)

# 初回のbuildを事前しておいてWebサーバの起動を高速化
pip_env.build(workspace)
