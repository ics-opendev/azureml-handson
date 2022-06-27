from azureml.core import Workspace, Experiment, Run

# ワークスペースを取得
workspace = Workspace.from_config()

# デプロイ対象の実験を取得
experiment = Experiment(workspace=workspace, name='pytorch')

# もっともlossが低いRunIDを設定
run = Run(experiment, '')

# モデル登録
run.register_model(
    model_name='handson-model',
    model_path='outputs/model.pth',
    model_framework='Custom',
    model_framework_version='1',
    description='handson model'
)