from azureml.core import Workspace, Experiment, ScriptRunConfig, Dataset, Environment

# ワークスペースを取得
workspace = Workspace.from_config()

# 作成済みのコンピューティングを取得
compute = workspace.compute_targets['cluster-takahashi-handson']

# 環境の取得
env = Environment.get(workspace, 'handson-env')

# 新たな実験を作成
experiment = Experiment(workspace=workspace, name='dataset')

# FileDatasetを取得
cifar10 = Dataset.get_by_name(workspace, name='cifar10', version='latest')

# トレーニングスクリプトを実行構成を定義
config = ScriptRunConfig(
    source_directory='src',
    script='dataset.py',
    compute_target=compute,
    arguments=[
        '--mount_data_path', cifar10.as_named_input('mount_data').as_mount(),
        '--download_data_path', cifar10.as_named_input('download_data').as_download()
    ],
    environment=env
)

# 実験を実行する
run = experiment.submit(config)

# Jobへの直接アクセスURLを表示することも可能です
job_url = run.get_portal_url()
print(job_url)