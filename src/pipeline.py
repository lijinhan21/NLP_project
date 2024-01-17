from LLM_refiner import LLM_refiner
from diffusers import StableDiffusionPipeline

def pipeline():
    # pipe = StableDiffusionPipeline.from_pretrained("/share/ljh", local_files_only=True).to("cuda")
    while(1):
        original, prompt = LLM_refiner()
        
        print("original message=", original, "final prompt=", prompt)
        en_pos = prompt.rfind(':')
        zh_pos = prompt.rfind('：')
        pos = max(en_pos, zh_pos)
        if pos != -1:
            prompt = prompt[pos + 3:] # 处理LLM输出额外多了一些东西的情况
        prompt = prompt.replace(' ', '')
        
        print("prompt = ", prompt)
        image = pipe(prompt, guidance_scale=10).images[0]  
        image.save("{}.png".format(prompt[:5]))
        print("saved refined image name is: ", "{}.png".format(prompt[:5]))
        
        image = pipe(original, guidance_scale=10).images[0]  
        image.save("old_{}.png".format(prompt[:5]))
        print("saved old image name is: ", "old_{}.png".format(prompt[:5]))
        
if __name__ == '__main__':
    while(1):
        try:
            pipeline()
        except:
            continue