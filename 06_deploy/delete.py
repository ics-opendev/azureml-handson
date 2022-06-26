from azureml.core import Workspace
from azureml.core.webservice import LocalWebservice

workspace = Workspace.from_config()
# コンピューティングインスタンス終了時に消えますが、念のため削除
local_service = LocalWebservice(workspace=workspace, name="handson-local-webservice")
local_service.delete()

# ACIで作ったWebServiceはエンドポイントに登録されるため、削除するまで永続的に残り続けます。
aci_service = Webservice(workspace=workspace, name="handson-aci-webservice")
aci_service.delete()
