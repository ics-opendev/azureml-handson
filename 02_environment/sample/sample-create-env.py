from azureml.core import Environment

# Environment の document
# https://docs.microsoft.com/ja-jp/python/api/azureml-core/azureml.core.environment(class)?view=azure-ml-py

# requirementsを元を作成
pip_env = Environment.from_pip_requirements('<name>', '<requirements-path>')

# conda定義を元に作成
conda_env = Environment.from_conda_specification('<name>', '<conda.yml-path>')

# コンピューティングインスタンスやローカルPCのconda環境から作成
local_conda_env = Environment.from_existing_conda_environment('<name>', '<condaの環境名>')

# dockerfileの中にconda もしくは pip の定義内容で作成 (dockerfileの指定がない場合は標準が利用されます)
docker_env = Environment.from_dockerfile('<name>', '<dockerfile-path>', conda_specification=None, pip_requirements=None)
