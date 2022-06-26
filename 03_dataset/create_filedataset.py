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
