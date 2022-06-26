import torch
import torchvision
import torchvision.transforms as transforms
import argparse
from azureml.core import Run, Dataset

if __name__ == '__main__':
    # FileDatasetのパスをコマンドライン引数で取得
    parser = argparse.ArgumentParser()
    parser.add_argument('--mount_data_path', type=str)
    parser.add_argument('--download_data_path', type=str)
    args = parser.parse_args()
    
    # マウントされたパスを表示
    print(f'--mount_data_path: {args.mount_data_path}')
    # ダウンロードされたパスを表示
    print(f'--download_data_path: {args.download_data_path}')

    # NOTE: パスを使ってファイル読み込み等で使用
    trainset = torchvision.datasets.CIFAR10(
        root=args.mount_data_path, # or args.download_data_path
        train=True,
        download=False
    )

    # 表形式データセットの利用
    workspace = Run.get_context(allow_offline=False).experiment.workspace

    # データを取得 (バージョン指定したい場合は数値を指定)
    iris = Dataset.get_by_name(workspace, name='iris', version='latest')

    # 前処理を入れての利用も可
    df = iris.to_pandas_dataframe()
    print(df.describe())
