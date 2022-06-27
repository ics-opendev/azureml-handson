from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment, Dataset, Run
from azureml.train.hyperdrive import normal, uniform, choice
from azureml.train.hyperdrive import RandomParameterSampling
from azureml.train.hyperdrive import PrimaryMetricGoal
from azureml.train.hyperdrive import MedianStoppingPolicy
from azureml.train.hyperdrive import HyperDriveConfig
from azureml.core.authentication import InteractiveLoginAuthentication


if __name__ == '__main__':
    # 認証情報を取得
    interactive_auth = InteractiveLoginAuthentication(tenant_id='')

    # ワークスペースの取得
    workspace = Workspace.from_config(auth=interactive_auth)
    
    # データを取得 (バージョン指定したい場合は数値を指定)
    dataset = Dataset.get_by_name(workspace, name='cifar10')

    # ローカル仮想環境を指定
    env = Environment('user-managed-env')
    env.python.user_managed_dependencies = True
    env.python.interpreter_path = ''

    # 実行内容を定義
    run_config = ScriptRunConfig(
        source_directory='./src',
        script='train.py',
        environment=env,
        compute_target='local',
        arguments=['--data_path', dataset.as_download(''),
        '--learning_rate', 0.003,
        '--momentum', 0.92]
    )

    # 実験を作成
    experiment = Experiment(workspace=workspace, name='pytorch')

    # 実行
    run = experiment.submit(run_config)

    aml_url = run.get_portal_url()
    print("ローカルPCで実行しました")
    print("")
    print(aml_url)
    run.wait_for_completion(show_output=True)
