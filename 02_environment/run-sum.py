from azureml.core import Workspace, Experiment, ScriptRunConfig
from azureml.core import Environment

# ワークスペースを取得
workspace = Workspace.from_config()

# 作成済みのコンピューティングを取得
compute = workspace.compute_targets['']

# 新たな実験を作成
experiment = Experiment(workspace=workspace, name='sum')

# トレーニングスクリプトを実行構成を定義
config = ScriptRunConfig(
    source_directory='src',
    script='sum.py',
    compute_target=compute
)

# 実験を実行する
run = experiment.submit(config)

# Jobへの直接アクセスURLを表示することも可能です
job_url = run.get_portal_url()
print(job_url)