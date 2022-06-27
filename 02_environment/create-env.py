from azureml.core import Workspace
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies

# 環境の作成
handson_env = Environment(name="handson-env")

# pipから環境を作成
conda_dependencies = CondaDependencies()
conda_dependencies.add_pip_package("torch==1.10.1")

# conda dependenciesを設定
handson_env.python.conda_dependencies = conda_dependencies

# ワークスペースを取得
workspace = Workspace.from_config()

# 環境をワークスペースに登録
handson_env.register(workspace)
