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

class Classifier(torch.nn.Module):
    def __init__(self, num_labels=2):
        super(Classifier, self).__init__()
        self.tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
        self.embedder = AutoModelForMaskedLM.from_pretrained("neuralmind/bert-base-portuguese-cased")

        self.dense = torch.nn.Linear(self.embedder.config.hidden_size, num_labels)
    
    def forward(self, text):
        tokens = self.tokenizer(text, return_tensors='pt', padding="max_length", truncation=True).to(self.embedder.device)
        outputs = self.embedder(**tokens)

        lhs = outputs.last_hidden_state
        cls_output = lhs[:, 0, :]

        return self.dense(cls_output)

class Data(Dataset):
    def __init__(self, data, task="hate"):
        super().__init__()
        self.data = data
        self.data["annotator1_moralA"] = self.data["annotator1_moralA"].apply(lambda x: x.replace("LM","NM"))
        self.task = task
        targets = ["HP", "FN", "FP", "LN", "LP", "AN", "AP", "PN" ,"PP", "NM"]
        self.target_mappings = {target: i for i, target in enumerate(targets)}
        
    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        row = self.data.iloc[index]
        text = row["comment"]
        if self.task == "hate":
            label = row["hate_label"]
        else:
            label = row["annotator1_moralA"]
            label = self.target_mappings[label]
        
        return text, label

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
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
    classifier = Classifier(num_labels=2 if task == "hate" else 10).to(device)
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
