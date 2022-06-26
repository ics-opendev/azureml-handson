from model import Net
import argparse
import torch
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

if __name__ == "__main__":
    # 引数の解析
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_path',
        type=str
    )
    args = parser.parse_args()

    # CIFAR10 の 前処理
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    trainset = torchvision.datasets.CIFAR10(
        root='../data',
        train=True,
        download=True,
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
        lr=0.003,
        momentum=0.92,
    )

    # トレーニング
    for epoch in range(args.num_epochs):
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            if i % 2000 == 1999:
                loss = running_loss / 2000
                print(f'epoch={epoch + 1}, batch={i + 1:5}: loss {loss:.2f}')
                running_loss = 0.0
    print('学習が完了しました')