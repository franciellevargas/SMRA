import pandas as pd
import torch
from dataset_model import Data, Classifier
from torch.utils.data import DataLoader


with torch.no_grad():
    preds = []
    all_labels = []
    all_texts = []

TASK = "hate"
data = pd.read_csv("HateBR-MoralXplain-Dataset.csv")
train = data.sample(frac=0.2, random_state=12)
val_test = data.drop(train.index)

val = val_test.sample(frac=0.10, random_state=12)
test = val_test.drop(val.index)

test_set = Data(test, TASK)
test_loader = DataLoader(test_set, batch_size=4, shuffle=False)

model = Classifier(2 if TASK == "hate" else 11)
model.load_state_dict(torch.load("best_model_1e-05_1_hate.pth" if TASK =="hate" else "best_model_1e-05_3_moral.pth"))

preds = []
for _, (texts, labels) in enumerate(test_loader):
    
    logits = model(texts)
    preds.extend(torch.argmax(logits, dim=1).detach().cpu().numpy())
    #all_labels.extend(labels)

test["bert_pred"] = preds
test.to_csv(f"bert_port_{TASK}.csv", index=False)