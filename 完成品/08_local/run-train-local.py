from azureml.core import Workspace, Experiment, ScriptRunConfig, Environment, Dataset, Run
from azureml.train.hyperdrive import normal, uniform, choice
from azureml.train.hyperdrive import RandomParameterSampling
from azureml.train.hyperdrive import PrimaryMetricGoal
from azureml.train.hyperdrive import MedianStoppingPolicy
from azureml.train.hyperdrive import HyperDriveConfig
from azureml.core.authentication import InteractiveLoginAuthentication


if __name__ == '__main__':
    # 認証情報を取得
    interactive_auth = InteractiveLoginAuthentication(tenant_id='4c208798-b379-43c6-b1a0-1c8a52a08e52')

    # ワークスペースの取得
    ws = Workspace.from_config(auth=interactive_auth)
    
    # データを取得 (バージョン指定したい場合は数値を指定)
    dataset = Dataset.get_by_name(ws, name='cifar10', version='latest')

    # ローカル仮想環境を指定
    env = Environment('user-managed-env')
    env.python.user_managed_dependencies = True
    env.python.interpreter_path = 'C:\\Users\\Admin\\Anaconda3\\envs\\azureml_37\\python'

    # 実行内容を定義
    run_config = ScriptRunConfig(
        source_directory='./src',
        script='train.py',
        environment=env,
        compute_target='local',
        arguments=['--data_path', dataset.as_download('C:\\Users\\Admin\\Desktop\\handson\\08_local\\dataset1'),
        '--learning_rate', 0.003,
        '--momentum', 0.92]
    )

    # 実験を作成
    experiment = Experiment(workspace=ws, name='pytorch')

    # 実行
    run = experiment.submit(run_config)

    aml_url = run.get_portal_url()
    print("ローカルPCで実行しました")
    print("")
    print(aml_url)
    run.wait_for_completion(show_output=True)
