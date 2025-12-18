from transformers import AutoTokenizer, AutoModelForMaskedLM
from torch.utils.data import Dataset
import torch

class Classifier(torch.nn.Module):
    def __init__(self, num_labels=2):
        super(Classifier, self).__init__()
        self.tokenizer = AutoTokenizer.from_pretrained("neuralmind/bert-base-portuguese-cased")
        self.embedder = AutoModelForMaskedLM.from_pretrained("neuralmind/bert-base-portuguese-cased")

        self.dense = torch.nn.Linear(self.embedder.config.hidden_size, num_labels)
    
    def forward(self, text):
        tokens = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True).to(self.embedder.device)
        outputs = self.embedder(**tokens, output_hidden_states=True, return_dict=True)

        lhs = outputs.hidden_states[-1]
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