import torchvision
import torchvision.transforms as transforms
from azureml.core import Workspace
from azureml.core import Dataset
from azureml.data.datapath import DataPath

# ローカルにCIFAR 10 をダウンロード 
trainset = torchvision.datasets.CIFAR10(
    root='./cifar10',
    train=True,
    download=True,
    transform=torchvision.transforms.ToTensor()
)

# ワークスペースを取得
workspace = Workspace.from_config()

# 保存先のデータストアを取得（今回は既定）
datastore = workspace.get_default_datastore()

# 保存先のパスを生成
save_path = DataPath(datastore, f'datasets/cifar10/1')

# データストアへ保存 
file_data = Dataset.File.upload_directory(
    src_dir='cifar10',
    target=save_path
)

# ワークスペースのデータとして登録
file_data.register(
    workspace=workspace,
    name='cifar10',
    description='cifar10 training data',
    create_new_version=True
)