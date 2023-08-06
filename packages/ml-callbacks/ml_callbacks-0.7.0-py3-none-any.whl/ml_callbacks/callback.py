from ml_callbacks.api_client import ApiClient

class Callback:
    name = ""
    arch = ""
    current = "init"
    baseUrl = ""
    epoch = 0
    total_epochs = 0
    train_batch = 0
    train_total_batch = 0

    script = ""
    
    best_val_acc = 0
    
    api = None
    # http://192.168.0.108:5000
    # https://mlai.endev.lt
    def __init__(self, name, arch, total_epochs, script, base_url="http://192.168.0.108:5000"):
        self.arch = arch
        self.name = name
        self.baseUrl = base_url
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
        self.api.afterEpoch(
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
        self.api.afterIteration(self.train_batch)
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
        self.api.setStatus("Ended", None)
        self.print_state()
        
    def on_start(self):
        self.current = "on_start"
        self.api.register()
        self.api.setStatus("Running", None)
        self.api.saveScript(self.script)
        self.print_state()
    
    def failed(self, error):
        self.current = "failed"
        self.api.setStatus("Failed", error)
        self.print_state()
        
    def on_model_saving(self, val_acc):
        self.current = "on_model_saving"        
        if self.best_val_acc <= val_acc or self.total_epochs == self.epoch:
            self.api.setStatus("Model Saving", None)
            self.best_val_acc = val_acc
            
            # path = self.api.getSavePath()
            # if self.arch == "pytorch":
            #     torch.save(model.state_dict(), path)
        
        self.print_state()
        
    def print_state(self): pass
