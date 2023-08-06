from ml_callbacks.api_client import ApiClient
from ml_callbacks.enviroment_callback import EnviromentInterface

class Callback:
    name = ""
    enviroment_callback = None
    current = "init"
    epoch = 0
    total_epochs = 0
    train_batch = 0
    train_total_batch = 0
    best_val_acc = 0

    script = ""
    api = None

    def __init__(self, 
        name, 
        arch, 
        total_epochs, 
        script, 
        enviroment_callback: EnviromentInterface,
        base_url="https://mlai.endev.lt"):

        self.enviroment_callback = enviroment_callback
        self.name = name
        self.total_epochs = total_epochs
        self.script = script
        self.api = ApiClient(name, base_url)
        
    def on_train_begin(self):
        self.current = "on_train_begin"
        self.print_state()
        
    def on_val_begin(self):
        self.current = "on_val_begin"
        self.print_state()
        
    def on_train_end(self):
        self.current = "on_train_end"
        self.train_batch = 0
        self.print_state()
        
    def on_val_end(self):
        self.current = "on_val_end"
        self.print_state()
        
    def on_epoch_begin(self):
        self.current = "on_epoch_begin"
        self.epoch += 1
        self.print_state()
        
    def on_epoch_end(self, train_acc, train_loss, train_time, val_acc, val_loss, val_time):
        self.current = "on_epoch_end"
        self.api.after_epoch(
            self.epoch,
            train_acc,
            train_loss,
            train_time,
            val_acc,
            val_loss,
            val_time
        )
        self.print_state()
        
    def on_train_batch_begin(self):
        self.train_batch += 1
        self.api.after_iteration(self.train_batch)
        self.current = "on_train_batch_begin"
        self.print_state()
        
    def on_train_batch_end(self):
        self.current = "on_train_batch_end"
        if (self.train_total_batch < self.train_batch):
            self.train_total_batch = self.train_batch
        self.print_state()
        
    def on_val_batch_begin(self):
        self.current = "on_val_batch_begin"
        self.print_state()
        
    def on_val_batch_end(self):
        self.current = "on_val_batch_end"
        self.print_state()
        
    def on_train_loss_begin(self):
        self.current = "on_train_loss_begin"
        self.print_state()
        
    def on_train_loss_end(self):
        self.current = "on_train_loss_end"
        self.print_state()
        
    def on_val_loss_begin(self):
        self.current = "on_val_loss_begin"
        self.print_state()
        
    def on_val_loss_end(self):
        self.current = "on_val_loss_end"
        self.print_state()
        
    def on_step_begin(self):
        self.current = "on_step_begin"
        self.print_state()
        
    def on_step_end(self):
        self.current = "on_step_end"
        self.print_state()
        
    def on_end(self):
        self.current = "on_end"
        self.api.set_status("Ended", None)
        self.print_state()
        
    def on_start(self):
        self.current = "on_start"
        self.api.register()
        self.api.set_status("Running", None)
        self.api.save_script(self.script)
        self.print_state()
    
    def failed(self, error):
        self.current = "failed"
        self.api.set_status("Failed", error)
        self.print_state()
        
    def on_model_saving(self, model, val_acc):
        self.current = "on_model_saving"        
        if self.best_val_acc <= val_acc or self.total_epochs == self.epoch:
            self.api.set_status("Model Saving", None)
            self.best_val_acc = val_acc
            
            path = self.api.get_save_path()
            self.enviroment_callback.model_saving(model, path)
        
        self.print_state()
        
    def print_state(self): pass
