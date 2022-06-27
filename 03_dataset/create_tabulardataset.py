from azureml.core import Workspace, Datastore, Dataset
from azureml.data.datapath import DataPath

# ワークスペースの取得
workspace = Workspace.from_config()

# 保存先のデータストアを取得（今回は既定）
datastore = workspace.get_default_datastore()

# データストアへ保存
dataset = Dataset.File.upload_directory(
    src_dir='csv',
    target=DataPath(datastore, f'datasets/iris/1'))

# 保存したデータのパスを生成
datastore_path = DataPath(datastore, f'datasets/iris/1/iris.csv')

# テーブルデータセットとして読み込み
tabular_dataset = Dataset.Tabular.from_delimited_files(path=datastore_path)

# URLでも登録可能
# tabular_dataset = Dataset.Tabular.from_delimited_files(path='https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

# ワークスペースのデータセットに登録
