import gc
import time
import numpy as np
import torch

# Logs - Helpful for plotting after training finishes
train_logs = {"loss" : [], "accuracy" : [], "time" : []}
val_logs = {"loss" : [], "accuracy" : [], "time" : []}

class PyTorchTraining:
    def train_one_epoch(
            self,
            model, 
            device, 
            train_data_loader, 
            optimizer, 
            loss_func, 
            acc_func, 
            callback
        ):
        # training begin event
        callback.on_train_begin()
        
        ### Local Parameters
        epoch_loss = []
        epoch_acc = []
        start_time = time.time()
        
        ### Iterating over data loader
        for images, labels in train_data_loader:
            # On bach begin
            callback.on_train_batch_begin()
            
            # Loading images and labels to device
            images = images.to(device)
            labels = labels.to(device)
            labels = labels.reshape((labels.shape[0], 1)) # [N, 1] - to match with preds shape
            
            # Reseting Gradients
            optimizer.zero_grad()
            
            # Forward
            preds = model(images)
            
            callback.on_train_loss_begin()
            
            # Calculating Loss
            _loss = loss_func(preds, labels)
            loss = _loss.item()
            epoch_loss.append(loss)
            
            # Calculating Accuracy
            acc = acc_func(preds, labels)
            epoch_acc.append(acc)
            
            # Backward
            _loss.backward()
            
            callback.on_train_loss_end()
            
            # optimizer step begin event
            callback.on_step_begin()
            
            optimizer.step()
            
            # optimizer step end event
            callback.on_step_end()
            
            # On bach end
            callback.on_train_batch_end()
        
        ### Overall Epoch Results
        end_time = time.time()
        total_time = end_time - start_time
        
        ### Acc and Loss
        epoch_loss = np.mean(epoch_loss)
        epoch_acc = np.mean(epoch_acc)

        ### Storing results to logs
        train_logs["loss"].append(epoch_loss)
        train_logs["accuracy"].append(epoch_acc)
        train_logs["time"].append(total_time)
        
        # training begin event
        callback.on_train_end()
            
        return epoch_loss, epoch_acc, total_time

    def val_one_epoch(
            self,
            model,
            device,
            val_data_loader,
            loss_func, 
            acc_func, 
            callback
        ):
        # validation begin event
        callback.on_val_begin()                
        
        ### Local Parameters
        epoch_loss = []
        epoch_acc = []
        start_time = time.time()
        
        ###Iterating over data loader
        for images, labels in val_data_loader:
            # On bach start
            callback.on_val_batch_begin()
            
            #Loading images and labels to device
            images = images.to(device)
            labels = labels.to(device)
            labels = labels.reshape((labels.shape[0], 1)) # [N, 1] - to match with preds shape
            
            #Forward
            preds = model(images)
            
            callback.on_val_loss_begin()
            
            #Calculating Loss
            _loss = loss_func(preds, labels)
            loss = _loss.item()
            epoch_loss.append(loss)
            
            #Calculating Accuracy
            acc = acc_func(preds, labels)
            epoch_acc.append(acc)
            
            callback.on_val_loss_end()
            
            # On bach end
            callback.on_val_batch_end()
        
        ###Overall Epoch Results
        end_time = time.time()
        total_time = end_time - start_time
        
        ###Acc and Loss
        epoch_loss = np.mean(epoch_loss)
        epoch_acc = np.mean(epoch_acc)
        
        ###Storing results to logs
        val_logs["loss"].append(epoch_loss)
        val_logs["accuracy"].append(epoch_acc)
        val_logs["time"].append(total_time)
            
        # epoch end event
        callback.on_val_end()
            
        return epoch_loss, epoch_acc, total_time

    def train_model(
            self,
            model,
            device,
            epochs,
            train_data_loader,
            val_data_loader,
            optimizer,
            train_loss_func,
            val_loss_func,
            acc_func,
            callback
        ):
        try:
            # On start
            callback.on_start()

            # Loading model to device
            model.to(device)

            for epoch in range(epochs):
                callback.on_epoch_begin()

                model.train()
                # Training
                train_loss, train_acc, train_time = self.train_one_epoch(
                    model=model,
                    device=device,
                    train_data_loader=train_data_loader,
                    optimizer=optimizer,
                    loss_func=train_loss_func,
                    acc_func=acc_func,
                    callback=callback
                )

                # Print Epoch Details
                print("\nTraining")
                print("Epoch {}".format(epoch+1))
                print("Loss : {}".format(round(train_loss, 4)))
                print("Acc : {}".format(round(train_acc, 4)))
                print("Time : {}".format(round(train_time, 4)))

                gc.collect()
                torch.cuda.empty_cache()

                # Validation
                print("\nValidating")
                with torch.no_grad():
                    model.eval()
                    val_loss, val_acc, val_time, = self.val_one_epoch(
                        model=model,
                        device=device,
                        val_data_loader=val_data_loader,
                        loss_func=val_loss_func,
                        acc_func=acc_func,
                        callback=callback
                    )
                    #Print Epoch Details
                    print("Epoch {}".format(epoch+1))
                    print("Loss : {}".format(round(val_loss, 4)))
                    print("Acc : {}".format(round(val_acc, 4)))
                    print("Time : {}".format(round(val_time, 4)))

                # On Epoch End
                callback.on_epoch_end(train_acc, train_loss, train_time, val_acc, val_loss, val_time)
                
                # On Model Saving
                callback.on_model_saving(model, val_acc)

            # On end
            callback.on_end()
        except Exception as e:
            # On Failed
            callback.failed(str(e))
            print(e)