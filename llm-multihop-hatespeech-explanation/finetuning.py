import pandas as pd
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.nn import CrossEntropyLoss
from torch.optim import AdamW
import sys
from tqdm import tqdm 
from copy import deepcopy
from dataset_model import Data, Classifier

data = pd.read_csv("HateBR-MoralXplain-Dataset.csv")
train = data.sample(frac=0.2, random_state=12)
val_test = data.drop(train.index)

val = val_test.sample(frac=0.10, random_state=12)
test = val_test.drop(val.index)

task = sys.argv[1]

train_set = Data(train, task=task)
val_set = Data(val, task=task)
train_loader = DataLoader(train_set, batch_size=8, shuffle=True)
val_loader = DataLoader(val_set, batch_size=8, shuffle=False)


best_model = None
best_epoch = -1
best_val_loss = 1000000
best_lr = -1
for lr in [0.01, 0.001, 0.0001, 0.00001, 0.05,0.005,0.0005, 0.00005]:
    classifier = Classifier(num_labels=2 if task == "hate" else 11).to(device)
    loss_fn = CrossEntropyLoss()#
    optimizer = AdamW(classifier.parameters(), lr=lr)

    for epoch in tqdm(range(5)):
        classifier.train()
        for _, (texts, labels) in enumerate(train_loader):
            optimizer.zero_grad()
            labels = labels.to(device)
            logits = classifier(texts)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()
        
        classifier.eval()
        with torch.no_grad():
            val_loss = 0
            counter = 0
            for _, (texts, labels) in enumerate(val_loader):
                labels = labels.to(device)
                logits = classifier(texts)
                loss = loss_fn(logits, labels)
                val_loss += loss.item()
                counter += 1
            
            val_loss /= counter
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_epoch = epoch
                best_lr = lr
                best_model = deepcopy(classifier.state_dict())

torch.save(best_model, f"best_model_{best_lr}_{best_epoch}_{task}.pth")    
