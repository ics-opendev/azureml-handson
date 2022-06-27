from azureml.core import Workspace
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies


# 環境の作成
handson_env = Environment(name="handson-env")

# pipから環境を作成
conda_dependencies = CondaDependencies()
conda_dependencies.add_pip_package("torch==1.10.1")
conda_dependencies.add_pip_package("azureml-sdk==1.42.0")
conda_dependencies.add_pip_package("azureml-dataprep==4.0.4")
conda_dependencies.add_pip_package("torchvision==0.11.2")
conda_dependencies.add_pip_package("pandas==1.4.3")

# conda dependenciesを設定
handson_env.python.conda_dependencies = conda_dependencies

# ワークスペースを取得
workspace = Workspace.from_config()

# 環境をワークスペースに登録
handson_env.register(workspace)

# 環境を事前にビルド
# handson_env.build(workspace)
