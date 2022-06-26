from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment, Dataset, Run

# ワークスペースの取得
workspace = Workspace.from_config()

# クラスターを取得
computing_cluster = workspace.compute_targets['cluster-takahashi-handson'] 

# データを取得 (バージョン指定したい場合は数値を指定)
dataset = Dataset.get_by_name(workspace, name='cifar10', version='latest')

# 環境の取得
env = Environment.get(workspace, 'handson-env')

# 実行内容を定義
config = ScriptRunConfig(
    source_directory='./src',
    script='train.py',
    environment=env,
    compute_target=computing_cluster,
    arguments=['--data_path', dataset.as_mount(),
    '--learning_rate', 0.003,
    '--momentum', 0.92]
)

# 実験を作成
experiment = Experiment(workspace=workspace, name='pytorch')

# 実行
run = experiment.submit(config)

# Jobへの直接アクセスURLを表示
job_url = run.get_portal_url()
print(job_url)

# モデル登録のために実行完了を待機
run.wait_for_completion()

# モデルを登録
run.register_model(
    model_name='handson-model',
    model_path='outputs/model.pth',
    model_framework='Custom',
    model_framework_version='1',
    description='handson model')

