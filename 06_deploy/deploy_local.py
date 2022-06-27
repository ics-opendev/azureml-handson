from azureml.core import Workspace
from azureml.core import Environment
from azureml.core.model import Model
from azureml.core.model import InferenceConfig
from azureml.core.webservice import LocalWebservice

# ���[�N�X�y�[�X���擾
workspace = Workspace.from_config()

# �f�v���C���̎w��
env = Environment.get(workspace, name="handson-webserver-env")

# ���_�\�����`
inference_config = InferenceConfig(
    environment=env,
    source_directory="",
    entry_script="",
)

# �f�v���C�������w��
deployment_config = LocalWebservice.deploy_configuration(port=6789)

# ���f���̎擾
model = Model(workspace, name="handson-model")

# �f�v���C�̎��{
service = Model.deploy(
    workspace,
    "handson-local-webservice",
    [model],
    inference_config,
    deployment_config,
    overwrite=True,
)
service.wait_for_deployment(show_output=True)