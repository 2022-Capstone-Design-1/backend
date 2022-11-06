import json
from tqdm import tqdm

with open('tasks/SpeechRecognition/ktelspeech/data/KtelSpeech/test-wav.json', 'r', encoding='utf-8') as f:
    metas = json.load(f)


domain_time = {}

for meta in tqdm(metas): 

    num_samples = meta["files"][0]["num_samples"]
    fname = meta["files"][0]["fname"]

    key = fname.split('/')[1]

    try:
        domain_time[key] += num_samples
    except:
        domain_time[key] = num_samples

domain_time = sorted(domain_time.items())

for k, v in domain_time:
    print(k, round(v / 16000 / 3600, 3), 'hrs')