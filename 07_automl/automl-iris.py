import logging
from azureml.core import Workspace, ScriptRunConfig, Experiment, Dataset
from azureml.train.automl import AutoMLConfig

# ワークスペースの取得
workspace = Workspace.from_config()

# データセットを取得
dataset = Dataset.get_by_name(workspace, 'iris')

# 分割内容を固定化したい場合はこちら
# training_data, validation_data = dataset.random_split(percentage=0.8, seed=1)

# 実験をワークスペースへ登録
experiment = Experiment(workspace=workspace, name='automl-iris')

# Auto MLの実行内容を定義
automl_classifier_config = AutoMLConfig(task=,
                                compute_target=,
                                training_data=,
                                validation_size=,
                                label_column_name=,
                                primary_metric=,
                                enable_early_stopping=,
                                experiment_timeout_hours=,
                                verbosity=logging.INFO)

# 実行
automl_run = experiment.submit(automl_classifier_config, show_output=True)

# 最高値のモデルを取得
best_run = automl_run.get_best_child()
print(best_run)

best_run.register_model(
    model_name='handson-automl-model',
    model_path='outputs/model.pkl',
    model_framework='Custom',
    model_framework_version='1',
    description='handson automl model'
)