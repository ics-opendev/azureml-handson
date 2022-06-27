from azureml.core import Workspace
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies

# ���̍쐬
handson_env = Environment(name="handson-env")

# pip��������쐬
conda_dependencies = CondaDependencies()
conda_dependencies.add_pip_package("torch==1.10.1")

# conda dependencies��ݒ�
handson_env.python.conda_dependencies = conda_dependencies

# ���[�N�X�y�[�X���擾
workspace = Workspace.from_config()

# �������[�N�X�y�[�X�ɓo�^
handson_env.register(workspace)
