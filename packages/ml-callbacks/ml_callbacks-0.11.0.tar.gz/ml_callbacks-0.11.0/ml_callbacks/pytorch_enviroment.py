from ml_callbacks.enviroment_callback import EnviromentInterface

import torch

class PytorchCallback(EnviromentInterface):
    def model_saving(self, model, path):
        torch.save(model.state_dict(), path)