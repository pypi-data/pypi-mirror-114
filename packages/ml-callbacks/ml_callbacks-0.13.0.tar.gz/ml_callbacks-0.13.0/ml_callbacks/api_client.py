import time
import uuid
from pprint import pprint
import ml_tracking
from ml_tracking.api import ml_model_api
from ml_tracking.model.register_model_run_command import RegisterModelRunCommand
from ml_tracking.model.iteration_update_command import IterationUpdateCommand
from ml_tracking.model.epoch_update_command import EpochUpdateCommand
from ml_tracking.model.save_notebook_code_command import SaveNotebookCodeCommand
from ml_tracking.model.status_update_command import StatusUpdateCommand

class ApiClient():
    name = ""
    session_id = 0
    configuration = None
    
    def __init__(self, name, base_url):
        self.name = name
        self.configuration = ml_tracking.Configuration(host = base_url)
        
    def register(self):
        if self.session_id == 0:
            with ml_tracking.ApiClient(self.configuration) as api_client:
                api_instance = ml_model_api.MlModelApi(api_client)
                model = RegisterModelRunCommand(
                    name=self.name,
                    u_id=str(uuid.uuid1())
                )
                api_response = api_instance.api_ml_model_register_post(register_model_run_command=model)
                self.session_id = api_response
            
    def after_iteration(self, iteration):
        with ml_tracking.ApiClient(self.configuration) as api_client:
            api_instance = ml_model_api.MlModelApi(api_client)
            model = IterationUpdateCommand(
                session_id=self.session_id,
                iteration=iteration
            )
            api_instance.api_ml_model_iteration_post(iteration_update_command=model)
            
    def after_epoch(self, epoch, train_accuracy, train_loss, train_time, val_accuracy, val_loss, val_time):
        with ml_tracking.ApiClient(self.configuration) as api_client:
            api_instance = ml_model_api.MlModelApi(api_client)
            model = EpochUpdateCommand(
                session_id=self.session_id,
                epoch=epoch,
                train_accuracy=float(train_accuracy),
                train_loss=float(train_loss),
                train_time=float(train_time),
                val_accuracy=float(val_accuracy),
                val_loss=float(val_loss),
                val_time=float(val_time),
            )
            api_instance.api_ml_model_after_epoch_post(epoch_update_command=model)
            
    def get_save_path(self):
        with ml_tracking.ApiClient(self.configuration) as api_client:
            api_instance = ml_model_api.MlModelApi(api_client)
            model = RegisterModelRunCommand(
                name=self.name,
                u_id=str(uuid.uuid1())
            )
            return api_instance.api_ml_model_save_path_session_id_get(session_id=self.session_id)
            
    def set_status(self, status, error):
        with ml_tracking.ApiClient(self.configuration) as api_client:
            api_instance = ml_model_api.MlModelApi(api_client)
            model = StatusUpdateCommand(
                session_id=self.session_id,
                status=status,
                error=error
            )
            api_instance.api_ml_model_update_status_post(status_update_command=model)
            
    def save_script(self, script):
        with ml_tracking.ApiClient(self.configuration) as api_client:
            api_instance = ml_model_api.MlModelApi(api_client)
            model = SaveNotebookCodeCommand(
                session_id=self.session_id,
                script=script
            )
            api_instance.api_ml_model_save_script_post(save_notebook_code_command=model)
