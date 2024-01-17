from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("/share/ljh", local_files_only=True).to("cuda")

prompt = '小桥流水人家，Van Gogh style'
image = pipe(prompt, guidance_scale=10).images[0]  
image.save("小桥.png")
