import pandas as pd
from tqdm import tqdm
import argparse
from prompts import definition, context, base_prompt_for_hate, base_prompt_for_moral, \
    hate_moral_combined, hate_moral_combined_with_definition, hate_with_definition, \
        moral_with_definition, hate_moral_combined_context, hate_context, moral_context
from llm_models import Model
parser = argparse.ArgumentParser()


parser.add_argument("--model", type=str, default="gpt-4o", choices=["gpt-4o", "llama70b"])
parser.add_argument("--prompt_type", type=str, default="base_hate", choices=["base_hate","hate_context","moral_context","hate_moral_context","base_moral","hate_moral", "hate_wdefinition", "hate_moral_wdefinition", "moral_wdefinition"])
parser.add_argument("--language", type=str, default="pt", choices=["en", "pt"])

args = parser.parse_args()

if args.language == "pt":
    data = pd.read_csv("HateBR-MoralXplain-Dataset.csv")
else:# en
    data = pd.read_csv("HateBR-MoralXplain-Dataset_end.csv")
model = Model(args.model)

if args.prompt_type == "base_hate":
    prompt = base_prompt_for_hate
elif args.prompt_type == "hate_context":
    prompt = hate_context.replace("{context}", context)
elif args.prompt_type == "base_moral":
    prompt = base_prompt_for_moral
elif args.prompt_type == "moral_context":
    prompt = moral_context.replace("{context}", context)
elif args.prompt_type == "hate_moral":
    prompt = hate_moral_combined
elif args.prompt_type == "hate_moral_context":
    prompt = hate_moral_combined_context.replace("{context}", context)
elif args.prompt_type == "hate_wdefinition":
    prompt = hate_with_definition.replace("{definition}", definition)
elif args.prompt_type == "hate_moral_wdefinition":
    prompt = hate_moral_combined_with_definition.replace("{definition}", definition)
elif args.prompt_type == "moral_wdefinition":
    prompt = moral_with_definition.replace("{definition}", definition)
else:
    raise Exception("prompt type not found")

prompts = []
for text in data["comment"]:
    temp_prompt = prompt.replace("{text}", text)
    prompts.append(temp_prompt)

data[f"{args.model}_{args.prompt_type}"] = model.run(prompts)
data.to_csv(f"{args.model}_preds/{args.prompt_type}.csv",index=False)
