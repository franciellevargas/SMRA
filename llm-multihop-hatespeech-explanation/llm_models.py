from openai import OpenAI
import os
from vllm import LLM, SamplingParams
import torch
from dotenv import load_dotenv
from tqdm import tqdm
import time
load_dotenv()

class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        if model_name == "gpt-4o":
            self.model = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        else:
            self.model = LLM("meta-llama/Llama-3.1-70B-Instruct",enable_prefix_caching=True, enable_chunked_prefill=True, gpu_memory_utilization=0.88,
                max_num_seqs=128,tokenizer_mode="auto",max_model_len=4096, tensor_parallel_size=torch.cuda.device_count())
            self.params = SamplingParams(temperature=0,max_tokens=1024)

    def run(self, prompts):
        if self.model_name == "gpt-4o":
            outputs = []
            for prompt in tqdm(prompts):
                try:
                    messages = [{"role": "system", "content": "You are a social psychologist specializing in moral psychology and hate speech classification"},
                {"role": "user","content": prompt}]
                    chat_completion = self.model.chat.completions.create(
                        messages=messages,
                        model="gpt-4o",
                        temperature=0
                    )
                except:
                    time.sleep(2)
                    messages = [{"role": "system", "content": "You are a social psychologist specializing in moral psychology and hate speech classification"},
                {"role": "user","content": prompt}]
                    chat_completion = self.model.chat.completions.create(
                        messages=messages,
                        model="gpt-4o",
                        temperature=0
                    )
                output = chat_completion.choices[0].message.content.strip()
                outputs.append(output)
        else:
            responses = self.model.chat(messages, self.params)
            outputs = [output.outputs[0].text for output in responses]
        return outputs
