from model import Net
from azureml.core import Run
import argparse
import torch
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import os

if __name__ == "__main__":
    # 実行を取得
    run = Run.get_context(allow_offline=False)
    
    # 引数の解析
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_path',
        type=str,
        help='Path to the training data'
    )
    parser.add_argument(
        '--num_epochs',
        type=int,
        default=2,
        help='number of epochs to train'
    )
    parser.add_argument(
        '--learning_rate',
        type=float,
        default=0.001,
        help='Learning rate for SGD'
    )
    parser.add_argument(
        '--momentum',
        type=float,
        default=0.9,
        help='Momentum for SGD'
    )
    args = parser.parse_args()

    # CIFAR10 の 前処理
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    trainset = torchvision.datasets.CIFAR10(
        root=args.data_path,
        train=True,
        download=False,
        transform=transform,
    )
    trainloader = torch.utils.data.DataLoader(
        trainset,
        batch_size=4,
        shuffle=True,
        num_workers=2
    )

    # ネットワークを読み込み
    net = Net()
    # 損失関数を定義
    criterion = torch.nn.CrossEntropyLoss()
    # optimizerの作成
    optimizer = optim.SGD(
        net.parameters(),
        lr=args.learning_rate,
        momentum=args.momentum,
    )

    # トレーニング
    for epoch in range(args.num_epochs):
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            # 勾配を0に初期化
            optimizer.zero_grad()

            # 順伝搬、逆伝搬、パラメータ更新
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # 統計情報を出力
            running_loss += loss.item()
            if i % 2000 == 1999:
                loss = running_loss / 2000 # 2000ミニバッチごとに出力
                run.log('loss', loss)
                print(f'epoch={epoch + 1}, batch={i + 1:5}: loss {loss:.2f}')
                running_loss = 0.0
    print('Finished Training')

    # NOTE: 実行環境のストレージにモデル保存
    torch.save(net.state_dict(), 'outputs/model.pth')

    # NOTE: 実行環境がリモートの場合は削除されるため手動でJobへアップロード
    run.upload_file('outputs/model.pth', 'outputs/model.pth')
    print('Saved Model')