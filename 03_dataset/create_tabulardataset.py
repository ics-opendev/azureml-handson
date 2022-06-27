from azureml.core import Workspace, Datastore, Dataset
from azureml.data.datapath import DataPath

# ワークスペースの取得
workspace = Workspace.from_config()

# テーブルデータセットとして読み込み
tabular_dataset = Dataset.Tabular.from_delimited_files(path='https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

# ワークスペースのデータセットに登録
