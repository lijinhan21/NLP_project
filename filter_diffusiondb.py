import numpy as np
import json
import os
from eval.simple_inference import MetricModel

def is_high_quality(pic_name, prompt, metric):
    aesthetic, clip = metric.getScore(pic_name, prompt)
    good = aesthetic > 5 and clip > 0.2
    if good:
        print("is good prompt!!!!!!!!!Yay!!!!!")
    return good, (aesthetic, clip)

def evaluate(base_folder_name, part_name):
    metric = MetricModel()
    with open(os.path.join(base_folder_name, part_name, '{}.json'.format(part_name))) as f:
        data = json.load(f)
    good_prompt = []
    num_skip = 0
    for idx, (pic_name, pic_dict) in enumerate(data.items()):
        prompt = pic_dict['p']
        print(pic_name, idx, prompt)
        if len(prompt) > 250:
            num_skip += 1
            continue
        high_quality, scores = is_high_quality(os.path.join(base_folder_name, part_name, pic_name), prompt, metric)
        if high_quality:
            # save prompt & pic_name
            good_prompt.append({'prompt': prompt, 'pic': pic_name, 'score': scores, 'part': part_name})
        if idx % 100 == 0:
            print('%d/%d'%(idx, len(data)))
    print('number of good prompts %d/%d'%(len(good_prompt), len(data)))
    print("skip", num_skip)
    print(part_name, 'finished')
    # with open('good_prompt_{}.json'.format(part_name), 'w', encoding='utf-8') as file_obj:
    #     json.dump(good_prompt, file_obj, ensure_ascii=False)
    return good_prompt

print("begin!")
base_folder_name = './diffusionDB'
part_names = ['part-000001', 'part-000002', 'part-000003', 'part-000004', 'part-000005']
good_prompts = []
for part_name in part_names:
    good_part = evaluate(base_folder_name, part_name)
    good_prompts.extend(good_part)
print("total_num_of_good_prompts", len(good_prompts))
with open('good_prompts.json', 'w', encoding='utf-8') as file_obj:
    json.dump(good_prompts, file_obj, ensure_ascii=False)