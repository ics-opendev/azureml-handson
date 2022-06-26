from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment, Dataset, Run
from azureml.train.hyperdrive import normal, uniform, choice
from azureml.train.hyperdrive import RandomParameterSampling
from azureml.train.hyperdrive import PrimaryMetricGoal
from azureml.train.hyperdrive import MedianStoppingPolicy
from azureml.train.hyperdrive import HyperDriveConfig

if __name__ == '__main__':
    # ワークスペースの取得
    workspace = Workspace.from_config()
    
    # クラスターを取得
    computing_cluster = workspace.compute_targets['cluster-takahashi-handson'] 

    # データを取得 (バージョン指定したい場合は数値を指定)
    dataset = Dataset.get_by_name(workspace, name='cifar10', version='latest')

    # 環境の取得
    env = Environment.get(workspace, 'handson-env')

    # 実行内容を定義
    run_config = ScriptRunConfig(
        source_directory='./src',
        script='train.py',
        environment=env,
        compute_target=computing_cluster,
        arguments=['--data_path', dataset.as_mount()]
    )

    # ------------ ここまではいつも通り ------------------- #

    # ---------------- ハイパーパラメータの調整 始まり ----------------- # 

    # ここからはカリキュラムを早く終わった人向け
    # ハイパーパラメータの調整クラス(HyperDriveConfig)を習得します
    # HyperDriveConfigは定義された探索範囲のハイパーパラメータを並列実行してくれます。
    # 使用時の変更点は１つ
    # ScriptRunConfig → HyperDriveConfig に変更するだけです(HyperDriveConfigの引数でScriptRunConfigが必要)
    # 詳細はMS公式ドキュメントを参照
    # https://docs.microsoft.com/ja-jp/azure/machine-learning/v1/how-to-tune-hyperparameters-v1

    # パラメータの探索空間を定義
    search_space = {
        'num_epochs': choice(1, 2),
        'learning_rate': uniform(0.001, 0.01),
        'momentum': uniform(0.85, 0.95)
    }

    # パラメータの空間サンプリング法の決定
    # その他のサンプリング方式は以下を参照
    # https://docs.microsoft.com/ja-jp/azure/machine-learning/v1/how-to-tune-hyperparameters-v1#sampling-the-hyperparameter-space
    param_sampling = RandomParameterSampling(search_space)

    # 主要メトリックの決定 05_training/src/train.py の 89行目で取得しているメトリック
    # 主要メトリックの詳細については以下を参照
    # https://docs.microsoft.com/ja-jp/azure/machine-learning/v1/how-to-tune-hyperparameters-v1#specify-primary-metric-to-optimize
    primary_metric_name="loss"
    # 最小化 or 最大化
    primary_metric_goal=PrimaryMetricGoal.MINIMIZE

    # 早期停止のポリシーを決定
    # 早期終了ポリシーについては以下を参照
    # https://docs.microsoft.com/ja-jp/azure/machine-learning/v1/how-to-tune-hyperparameters-v1#early-termination
    early_termination_policy = MedianStoppingPolicy(evaluation_interval=1, delay_evaluation=5)

    # コンピューティングリソースの割り当てについて
    # https://docs.microsoft.com/ja-jp/azure/machine-learning/v1/how-to-tune-hyperparameters-v1#create-and-assign-resources

    # ハイパーパラメータの試行回数
    max_total_runs = 4
    # コンピューティングの並列の上限
    max_concurrent_runs = 4
    # 実行時間の上限(今回は設定しない)
    max_duration_minutes = 0


    # ハイパーパラメーター調整の実行内容を定義
    hd_config = HyperDriveConfig(
        run_config=run_config, # ここでScriptRunConfigを設定
        hyperparameter_sampling=param_sampling,
        policy=early_termination_policy,
        primary_metric_name=primary_metric_name,
        primary_metric_goal=primary_metric_goal,
        max_total_runs=max_total_runs,
        max_concurrent_runs=max_concurrent_runs)
    
    # NOTE: 実務ではウォームスタートも利用することあるかと思います
    # https://docs.microsoft.com/ja-jp/azure/machine-learning/v1/how-to-tune-hyperparameters-v1#warm-start-hyperparameter-tuning-optional
    
    # 実験を作成
    experiment = Experiment(workspace=workspace, name='pytorch')

    # 実行
    hyperdrive_run = experiment.submit(hd_config)

    # モデル登録のために実行完了まで待機
    hyperdrive_run.wait_for_completion()

    # ---------------- ハイパーパラメータの調整 終わり ----------------- #

    # 最高値のモデルを取得 NOTE: 正しく取得できないMSに確認中
    #best_run = hyperdrive_run.get_best_run_by_primary_metric()

    # lossの最小値を取得してRunIDを取得
    metrics = hyperdrive_run.get_metrics()
    best_run_item = min(metrics.items(), key=lambda x: min(x[1]['loss']))
    best_run = Run.get(ws, best_run_item[0])

    # モデルを登録
    best_run.register_model(
        model_name='handson-model',
        model_path='outputs/model.pth',
        model_framework='Custom',
        model_framework_version='1',
        description='handson model')

