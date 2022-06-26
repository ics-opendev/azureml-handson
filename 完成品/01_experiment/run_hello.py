from azureml.core import Workspace, Experiment, ScriptRunConfig

# ワークスペースを取得
workspace = Workspace.from_config()

# 新たな実験を作成
experiment = Experiment(workspace=workspace, name='hello')

# 作成済みのコンピューティングを取得
# 表示名を入れると取得可能
compute = workspace.compute_targets['ins-takahashi-handson'] 

# トレーニングスクリプトを実行構成を定義
config = ScriptRunConfig(
    source_directory='src', # run-hello.py との相対パス
    script='hello.py', # source_directory との相対パス
    compute_target=compute # 実行するコンピューティングの名称
)

# 実験を実行する
run = experiment.submit(config)

# Jobへの直接アクセスURLを表示することも可能です
job_url = run.get_portal_url()
print(job_url)